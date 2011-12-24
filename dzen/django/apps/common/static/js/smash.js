(function() {
  /*
   * Returns the smash function that needs to get executed, which is bound to
   * the final smash URL, the original list of files, and the smash options.
   */
  function smashFactory(smash_params) {
    var smash_type = smash_params.type || 'javascript',
        files = getSmashableFiles(smash_type),
        url = smashURL(files, smash_params);
    
    switch (smash_type) {
      case 'stylesheet':
        return function() { smashStylesheet(url, files, smash_params); }

      case 'javascript':
      default:
        return function() { smashJavascript(url, files, smash_params); }
    }
  }

  /*
   * Asynchronously loads the smashed javascript URL using the script injection technique.
   * On failure, unless a custom 'on_error' method name is defined in the
   * smash_params object, we will synchronously load the files in the original
   * order that they appeared in the markup.
   */
  function smashJavascript(url, files, smash_params) {
    load(url).onError(window[smash_params.on_error] || function(error) {
      var chain = load(files[0]);

      for (var i = 1, length = files.length; i < length; i++) {
        chain.then(files[i]);
      }
    });
  }

  /*
   * Synchronously loads the styles using a document.write(). This assumes that
   * the smash style tags are a part of <head> (bad practice not to be there, so
   * don't even bother to adjust accordingly). On failure, we append the CSS into
   * the DOM and let the browser request the files when it's ready.
   *
   * Note: The failure condition will currently trigger a FOUC, so maybe we can
   * find a cleaner way to do this in the future.
   */
  function smashStylesheet(url, files, smash_params) {
    document.write(createCSSTag(url));

    // We can use an Image object's onerror event to determine if the smashed CSS
    // URL we wrote to the DOM came back with something other than a 200.
    var img = new Image();
    img.onerror = function() {
      var head = document.getElementsByTagName('head')[0];

      for (var i = 0, length = files.length; i < length; i++) {
        var cssLink = document.createElement('link');
        cssLink.setAttribute('rel', 'stylesheet');
        cssLink.setAttribute('type', 'text/css');
        cssLink.setAttribute('href', files[i]);
        head.appendChild(cssLink);
      }
    };
    img.src = url;
  }

  /*
   * Constructs a CSS <link> tag.
   */
  function createCSSTag(url) {
    return '<link rel="stylesheet" type="text/css" href="' + url + '"/>';
  }

  /*
   * Searches all <link> tags and returns a list of the URLs that were included
   * that had a rel attribute of {type}/wesumo, where {type} is either 'javascript'
   * or 'stylesheet'. For each matched smash link, we immediately append a '-parsed'
   * to the rel attribute so that subsequent calls to this method to not return
   * smash links we've already processed.
   */
  function getSmashableFiles(type) {
    var files = [],
        assets = document.getElementsByTagName('link');

    for (var i = 0, length = assets.length; i < length; i++) {
      var asset = assets[i];

      if (asset.rel && asset.rel.toLowerCase() == type + '/wesumo') {
        files.push(asset.href);
        asset.rel += '-parsed';
      }
    }

    return files;
  }

  /*
   * Constructs a smash URL in the format of:
   *
   * http(s)?://{smash_domain}/smash/{api_key}/{file}(@{file})*
   */
  function smashURL(files, smash_params) {
    return [
      smash_params.smash_domain || '//s.wesumo.com',
      'smash',
      encodeURIComponent(smash_params.key),
      encodeFileURLs(files).join('@')
    ].join('/');
  }

  /*
   * Make sure that the file URLs we include in the final smash URL are normalized
   * and URL-decoded. The normalization that we use allows the developer to use relative,
   * protocol-less, or absolute URL references in the smash link tags.
   */
  function encodeFileURLs(files) {
    (function(location) {
      'origin' in location || (location.origin = location.protocol + '//' + location.host);
    })(window.location);

    // Supports absolute, relative, and protocol-less URLs
    function normalizeURL(url) {
      var anchor = getAnchor(url);

      // no hostname and the path is absolute
      if (!anchor.hostname && anchor.pathname[0] == '/') {
        return window.location.origin + anchor.pathname;
      }

      return anchor.href;
    }

    return files.map(function(url) {
      return encodeURIComponent(normalizeURL(url));
    });
  }

  /*
   * Constructs an off-window anchor DOM element with the provided URL as its href.
   * This gives us a native parsed URL object that we can then use to do things like
   * look at the protocol, path, and query string.
   */
  function getAnchor(url) {
    var anchor = document.createElement('a');
    anchor.href = url;
    return anchor;
  }

  /*
   * Returns an object of the key=val pairs that appear in the query string.
   */
  function parseQueryString(query_string) {
    var result = {},
        key_val_pairs = query_string.split('&');

    for (var i = 0, length = key_val_pairs.length; i < length; i++) {
      var key_val_pair = key_val_pairs[i].split('=');
      result[key_val_pair[0]] = key_val_pair[1];
    }

    return result;
  }

  (function() {
    /* Copyright (c) 2010 Chris O'Hara <cohara87@gmail.com>. MIT Licensed */
    // Include the chain.js microframework (http://github.com/chriso/chain.js)
    function loadScript(a,b,c){var d=document.createElement("script");d.type="text/javascript",d.src=a,d.onload=b,d.onerror=c,d.onreadystatechange=function(){var a=this.readyState;if(a==="loaded"||a==="complete")d.onreadystatechange=null,b()},head.insertBefore(d,head.firstChild)}(function(a){a=a||{};var b={},c,d;c=function(a,d,e){var f=a.halt=!1;a.error=function(a){throw a},a.next=function(c){c&&(f=!1);if(!a.halt&&d&&d.length){var e=d.shift(),g=e.shift();f=!0;try{b[g].apply(a,[e,e.length,g])}catch(h){a.error(h)}}return a};for(var g in b){if(typeof a[g]==="function")continue;(function(e){a[e]=function(){var g=Array.prototype.slice.call(arguments);if(e==="onError"){if(d){b.onError.apply(a,[g,g.length]);return a}var h={};b.onError.apply(h,[g,g.length]);return c(h,null,"onError")}g.unshift(e);if(!d)return c({},[g],e);a.then=a[e],d.push(g);return f?a:a.next()}})(g)}e&&(a.then=a[e]),a.call=function(b,c){c.unshift(b),d.unshift(c),a.next(!0)};return a.next()},d=a.addMethod=function(d){var e=Array.prototype.slice.call(arguments),f=e.pop();for(var g=0,h=e.length;g<h;g++)typeof e[g]==="string"&&(b[e[g]]=f);--h||(b["then"+d.substr(0,1).toUpperCase()+d.substr(1)]=f),c(a)},d("chain",function(a){var b=this,c=function(){if(!b.halt){if(!a.length)return b.next(!0);try{null!=a.shift().call(b,c,b.error)&&c()}catch(d){b.error(d)}}};c()}),d("run",function(a,b){var c=this,d=function(){c.halt||--b||c.next(!0)},e=function(a){c.error(a)};for(var f=0,g=b;!c.halt&&f<g;f++)null!=a[f].call(c,d,e)&&d()}),d("defer",function(a){var b=this;setTimeout(function(){b.next(!0)},a.shift())}),d("onError",function(a,b){var c=this;this.error=function(d){c.halt=!0;for(var e=0;e<b;e++)a[e].call(c,d)}})})(this),addMethod("load",function(a,b){for(var c=[],d=0;d<b;d++)(function(b){c.push(function(c,d){loadScript(a[b],c,d)})})(d);this.call("run",c)});var head=document.getElementsByTagName("head")[0]||document.documentElement;
  }).apply(window);

  var smash_params = (function() {
    var script_tags = document.getElementsByTagName('script'),
        this_script = script_tags[script_tags.length - 1],
        query_string = getAnchor(this_script.src).hash.substr(1);

    return parseQueryString(query_string);
  })();

  smashFactory(smash_params)();
})();
