### alexlouden.com

Written using HTML5, [sass](http://sass-lang.com), [bourbon](http://bourbon.io) and [coffeescript](http://coffeescript.org), built using [cactus](https://github.com/eudicots/Cactus/). Uses Python 3.

### Development

```bash
pipenv install
pipenv shell
yarn global add coffee-script yuicompressor google-closure-compiler-js
gem install sass
cactus serve
```

### Deploy

```bash
cactus deploy
aws cloudfront create-invalidation --distribution-id E3DCULJZDC9TNR --profile alexlouden --path "/"
```