import shortid from 'shortid'
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, HEAD, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}
import AWS from 'aws-sdk'
const EP = new AWS.Endpoint('ams3.digitaloceanspaces.com')
const s3 = new AWS.S3({
  endpoint: EP,
  accessKeyId: KEY_ID,
  secretAccessKey: SECRET_KEY,
  region: 'ams3',
  signatureVersion: 'v4',
})

const myBucket = 'compsoc'
const signedUrlExpireSeconds = 60 * 5

async function handleRequest(request) {
  let url = new URL(request.url)
  if (request.method == 'OPTIONS') {
    return new Response(JSON.stringify({}), {
      status: 200,
      headers: corsHeaders,
    })
  }
  const id = shortid()
  url = s3.getSignedUrl('putObject', {
    Bucket: myBucket,
    Key: `media/${id}`,
    Expires: signedUrlExpireSeconds,
    ContentType: request.headers.get('Content-Type'),
  })
  return new Response(
    JSON.stringify({
      signed: url,
      access: `https://cdn.comp-soc.com/media/${id}`,
      id,
    }),
    {
      status: 200,
      headers: corsHeaders,
    },
  )
}
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})
