export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-y4dtlj6thn26xy28.us', // the auth0 domain prefix
    audience: 'http://127.0.0.1:5000/', // the audience set for the auth0 app
    clientId: 'J47SjndQpDdq9aXNEWGGDezCWzbiXru0', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
