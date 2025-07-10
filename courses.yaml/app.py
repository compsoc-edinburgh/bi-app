#! /bin/env python
from bs4 import BeautifulSoup
import bs4
from urllib.request import urlopen
import os
from typing import Optional, Any
import sys
import yaml
import datetime
import re


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# check_euclid_url sanity checks that real_url looks like a proper link to DRPS
def check_euclid_url(code: str, real_url: str):
    # Yes, unfortunately DRPS only supports HTTP. and not HTTPS.
    # The University of Edinburgh, everyone.
    prefix_len = len("http://www.drps.ed.ac.uk/")

    # This plucks out the "16-17" from e.g. http://www.drps.ed.ac.uk/16-17/dpt/cxinfr08013.htm
    year = real_url[prefix_len : prefix_len + 5]

    # Now we recreate the URL
    expected_euclid_url = f"http://www.drps.ed.ac.uk/{year}/dpt/cx{code.lower()}.htm"

    # And do an assertion
    if real_url != expected_euclid_url:
        eprint(f"Expected to see something like {expected_euclid_url}")
        eprint(f"Got this instead: {real_url}")
        sys.exit(1)


def deep_equals(left: dict[Any, Any], right: dict[Any, Any]):
    return yaml.safe_dump(left) == yaml.safe_dump(right)


def acronym_from_url(url: str):
    url_prefix = "https://course.inf.ed.ac.uk/"
    year_acronym = url[len(url_prefix) :].upper()
    parts = year_acronym.split("-", 1)
    if len(parts) == 2 and len(parts[0]) == 2 and parts[0].isdigit():
        return parts[1]
    else:
        return year_acronym


def set_action_output(output_name: str, value: str):
    """Sets the GitHub Action output to be used for subsequent jobs."""
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print("{0}={1}".format(output_name, value), file=f)


assert acronym_from_url("https://course.inf.ed.ac.uk/21-fnlp") == "FNLP"
assert acronym_from_url("https://course.inf.ed.ac.uk/iads") == "IADS"
assert acronym_from_url("https://course.inf.ed.ac.uk/22-nlu+") == "NLU+"
assert acronym_from_url("https://course.inf.ed.ac.uk/22-bai-icdm") == "BAI-ICDM"
assert acronym_from_url("https://course.inf.ed.ac.uk/bai-icdm") == "BAI-ICDM"
assert acronym_from_url("https://course.inf.ed.ac.uk/fo-bar") == "FO-BAR"


class Course(object):
    name: str = ""
    acronym: str = ""
    course_url: Optional[str] = None
    euclid_code: str = ""
    euclid_url: str = ""
    euclid_code2: Optional[str] = None
    euclid_url2: Optional[str] = None
    level: int = 0
    credits: int = 0
    year: str = ""
    delivery: str = ""
    delivery_ordinal: int = 0
    diet: str = ""
    cw_exam_ratio: Optional[list[int]] = None

    def __init__(self, soup: bs4.element.Tag):
        fields = soup.find_all("td")
        # print(fields)

        name_field = fields[0]
        self.name = name_field.text

        # get acronym from url
        url_elem = name_field.find("a", href=True)
        if url_elem is not None:
            url_str = url_elem["href"]
            self.acronym = acronym_from_url(url_str)
            self.course_url = url_str

        euclid_ele = fields[1]
        self.euclid_code = euclid_ele.text
        self.euclid_url = fields[1].find("a", href=True)["href"]
        check_euclid_url(self.euclid_code, self.euclid_url)

        # Add the shadow drps link too
        euclid_ele2 = fields[2]
        if euclid_ele2.text != "":
            self.euclid_code2 = euclid_ele2.text
            self.euclid_url2 = fields[2].find("a", href=True)["href"]
            check_euclid_url(self.euclid_code2, self.euclid_url2)

        # NOTE(qaisjp): the acronym column is sometimes wrong. ITO pls fix
        # we prefer the real acronym, though, because it has correct capitalisation (e.g IoTSSC, not IOTSSC)
        # we do this by comparing string lengths
        sometimes_wrong_acronym = fields[3].text
        if sometimes_wrong_acronym.upper() == self.acronym or self.acronym == "":
            self.acronym = sometimes_wrong_acronym

        if self.acronym == "":
            print("Should never happen! No acronym for", self.name, self.euclid_code)

        self.level = int(fields[6].text)
        self.credits = int(fields[7].text)
        self.year = fields[8].text
        self.delivery = fields[9].text
        self.diet = fields[10].text

        if self.delivery == "SEM1":
            self.delivery_ordinal = 1
        elif self.delivery == "SEM2":
            self.delivery_ordinal = 2
        elif self.delivery == "YR":
            self.delivery_ordinal = 3
        else:
            self.delivery_ordinal = 4

        ratio = fields[11].text
        if ratio == "":
            self.cw_exam_ratio = None
        else:
            assert ratio.count("/") == 1
            cw, exam = map(int, ratio.split("/"))
            self.cw_exam_ratio = [cw, exam]

    def build_fields(self):
        return {
            "name": self.name,
            "euclid_code": self.euclid_code,
            "euclid_url": self.euclid_url,
            "euclid_code_shadow": self.euclid_code2,
            "euclid_url_shadow": self.euclid_url2,
            "acronym": self.acronym,
            "course_url": self.course_url,
            "level": self.level,
            "credits": self.credits,
            "delivery": self.delivery,
            "delivery_ordinal": self.delivery_ordinal,
            "year": self.year,
            "diet": self.diet,
            "cw_exam_ratio": self.cw_exam_ratio,
        }

    def __str__(self):
        return "{name}\t\t\t\t{acronym} ({course_url}) ({euclid_code})\t\t{delivery}\t\t{diet}\t\t{cw_exam_ratio}\t\tLevel {level}, {credits} credits".format(
            name=self.name,
            acronym=self.acronym,
            course_url=self.course_url,
            euclid_code=self.euclid_code,
            delivery=self.delivery,
            diet=self.diet,
            cw_exam_ratio=self.cw_exam_ratio,
            level=self.level,
            credits=self.credits,
        )


session_regex = re.compile(r".*drps.ed.ac.uk\/([0-9\-]*).*")


def main():
    usock = urlopen("http://course.inf.ed.ac.uk")

    b = BeautifulSoup(usock.read(), "html.parser")
    cTable = b.find("table", attrs={"class": "sortable"})
    if cTable is None:
        eprint("Failed to find table with class `sortable`")
        sys.exit(1)
    cBody = cTable.find("tbody")
    if not isinstance(cBody, bs4.element.Tag):
        eprint("Failed to find valid tbody")
        sys.exit(1)
    rows = cBody.find_all("tr")

    courses = list(map(Course, rows))

    dump_yaml = False
    if len(sys.argv) > 1:
        dump_yaml = sys.argv[1] == "--dump-yaml"
        dump_codes = sys.argv[1] == "--dump-codes"
        yaml_target = None
        if sys.argv[1] == "--auto-yaml":
            dump_yaml = True
            yaml_target = sys.argv[2]
    else:
        # This checks to make sure that any courses with an empty field
        # for exam diet has a cw_exam_ratio of "100/0"
        non_conform = False
        for course in courses:
            if (course.diet == "None") and (
                course.cw_exam_ratio is None or course.cw_exam_ratio[0] != 100
            ):
                if not non_conform:
                    non_conform = True
                    print(
                        "Issue: Exam diet unspecified despite cw-ratio being None or coursework ratio < 100:"
                    )
                    print("acronym (euclid)\t\tdelivery\t\tdiet\t\tratio")
                print(course)

        print()
        print()
        print("Call again with --dump-yaml to print out YAML")
        print(
            "Call again with --dump-codes year to print out the INFR codes for that year"
        )
        print(
            "Call again with --auto-yaml <filename> to read the file, compare contents, update the file, and print stuff out for GitHub Actions"
        )
        return

    if dump_yaml:
        infoNode = b.find("p", attrs={"class": "info noprint"})
        now = datetime.datetime.now()
        lastUpdate = "Unknown (assuming now: " + str(now) + ")"
        if isinstance(infoNode, bs4.element.Tag):
            lastUpdate_elem = infoNode.find("span", attrs={"class": "date"})
            if lastUpdate_elem is not None:
                lastUpdate = lastUpdate_elem.text

        out = ""
        out += "# This document was automatically generated\n"
        out += "# using data from http://course.inf.ed.ac.uk\n"
        out += "#\n"
        out += f"# Last update: {lastUpdate}\n\n"

        courses_out = {}
        for course in courses:
            courses_out[course.acronym.lower()] = course.build_fields()

        data = {}
        session_match = session_regex.match(courses[0].euclid_url)
        if session_match is None:
            eprint(
                "Failed to match session regex on first course URL:",
                courses[0].euclid_url,
            )
            sys.exit(1)
        data["session"] = "20" + session_match.group(1)
        data["list"] = courses_out
        data["last_update"] = now.isoformat()

        out += yaml.safe_dump(data, default_flow_style=False)

        if yaml_target == None:
            print(out)
            return

        if not os.path.isfile(yaml_target):
            eprint(f"File {yaml_target} does not exist.")
            sys.exit(1)
            return

        with open(yaml_target, "r") as f:
            old_data = yaml.safe_load(f)

        # Docs:
        # - https://github.community/t/perform-next-job-if-specific-step-of-previous-job-was-success/17329/2?u=qaisjp
        # - https://github.community/t/support-saving-environment-variables-between-steps/16230/2?u=qaisjp
        # - https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions#setting-an-output-parameter
        has_changed = not deep_equals(old_data["list"], data["list"])
        has_changed_str = str(has_changed).lower()
        set_action_output("has_changed", has_changed_str)

        eprint(f"courses.yaml changed? {has_changed_str}")

        with open(yaml_target, "w") as f:
            f.write(out)

    elif dump_codes:
        if len(sys.argv) < 3:
            print("Please provide a year: 1/2/3/4/P")
            return

        year = sys.argv[2]

        for course in courses:
            if course.year == year:
                # print(course.year, course.euclid_code, course.diet)
                print(course.euclid_code, end=" ")

    else:
        print("Unknown arg provided.")
        return


main()
