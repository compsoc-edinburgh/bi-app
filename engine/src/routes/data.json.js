import navigation from "../data/navigation.yml";
import courses from "../data/courses.yml";
import repo from "../data/repo.yml";
import settings from "../data/settings.yml";

export function get(req, res, next) {
  res.writeHead(200, {
    "Content-Type": "application/json"
  });

  res.end(
    JSON.stringify({
      navigation,
      courses,
      repo,
      settings
    })
  );
}
