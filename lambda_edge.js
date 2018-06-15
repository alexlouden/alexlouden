'use strict';
exports.handler = (event, context, callback) => {

    const response = event.Records[0].cf.response;
    const headers = response.headers;

    // Set new headers
    headers['strict-transport-security'] = [{key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubdomains; preload'}];
    headers['content-security-policy'] = [{key: 'Content-Security-Policy', value: "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; object-src 'none'; child-src 'self' https://*.youtube.com https://*.vimeo.com;"}];
    headers['x-content-type-options'] = [{key: 'X-Content-Type-Options', value: 'nosniff'}];
    headers['x-frame-options'] = [{key: 'X-Frame-Options', value: 'DENY'}];
    headers['x-xss-protection'] = [{key: 'X-XSS-Protection', value: '1; mode=block'}];
    headers['referrer-policy'] = [{key: 'Referrer-Policy', value: 'same-origin'}];

    // Pinned Keys are the Amazon intermediate: "s:/C=US/O=Amazon/OU=Server CA 1B/CN=Amazon"
    //   and LetsEncrypt "Let’s Encrypt Authority X1 (IdenTrust cross-signed)"
    headers['public-key-pins'] = [{key: 'Public-Key-Pins', value: 'pin-sha256="JSMzqOOrtyOT1kmau6zKhgT676hGgczD5VMdRMyJZFA="; pin-sha256="YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg="; max-age=1296001; includeSubDomains'}];

    callback(null, response);
};