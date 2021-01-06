const fdk = require('@fnproject/fdk');

const books = [
  {
    "isbn": "1",
    "title": "Java - The Complete Reference",
    "author": "Herbert Schildt"
  },
  {
    "isbn": "2",
    "title": "Effective Java",
    "author": "Joshua Bloch"
  },
  {
    "isbn": "3",
    "title": "Learning Python",
    "author": "Mark Lutz"
  },
  {
    "isbn": "4",
    "title": "JavaScript: The Definitive Guide",
    "author": "David Flanagan"
  },
  {
    "isbn": "5",
    "title": "Oracle SOA Suite 12c Handbook",
    "author": "Lucas Jellema"
  }
];

fdk.handle(function (input, ctx) {

  const APP_NAME = ctx.config.APP_NAME; //ctx.getConfig('APP_NAME');
  const FN_NAME = ctx.config.FN_NAME; //ctx.getConfig('FN_NAME');
  console.log('Inside App Name: %s | Function Name: %s | Language: Node \n', APP_NAME, FN_NAME);
  console.log('Response Content Type: ', ctx.responseContentType);
  let hctx = ctx.httpGateway;
  console.log('User agent: ', hctx.getHeader('User-Agent'));

  return books;
})
