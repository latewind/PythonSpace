(function(){
  var jquery_version = '2.1.4';
  var site_url = 'http://127.0.0.1:8000/';
  var static_url = site_url + 'static/';
  var min_width = 1;
  var min_height = 1;

  function bookmarklet(msg) {
      // Here goes our bookmarklet code
          // load CSS
    var css = jQuery('<link>');
    css.attr({
      rel: 'stylesheet',
      type: 'text/css',
      href: static_url + 'images/css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
    });
    jQuery('head').append(css);

    // load HTML
    box_html = '<div id="bookmarklet"><a href="#" id="close">×</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
    jQuery('body').append(box_html);
    jQuery('body').append('<div id="bookmarktip">'+'收藏'+'</div>');
      // close event
      jQuery('#bookmarklet #close').click(function(){
      jQuery('#bookmarklet').remove();
      });
          // find images and display them
     console.log(jQuery('img'))
    jQuery.each(jQuery('img'), function(index, image) {

      if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height)
      {
       jQuery(this).on({
       mouseenter:function(){
        console.log( image_url = jQuery(image).attr('src'))
        var top = jQuery(image).offset().top
        var left = jQuery(image).offset().left
        jQuery('#bookmarktip').css('top',top+"px")
        jQuery('#bookmarktip').css('left', left+"px")
        image_url = jQuery(image).attr('src');
        jQuery('#bookmarktip').attr('data-url',image_url)
        jQuery('#bookmarktip').show()
       },
       mouseleave:function(event){

       }});
      }

    });

       jQuery('#bookmarktip').click(function(e){
      selected_image = jQuery(this).attr('data-url');
      // hide bookmarklet
      // open new window to submit the image
      window.open(site_url +'images/create/?url='
                  + encodeURIComponent(selected_image)
                  + '&title=' + encodeURIComponent(jQuery('title').text()),
                  '_blank');
    });



    }
 // Check if jQuery is loaded
  if(typeof window.jQuery != 'undefined') {
    bookmarklet();
  } else {
    // Check for conflicts
    var conflict = typeof window.$ != 'undefined';
    // Create the script and point to Google API
    var script = document.createElement('script');
    script.setAttribute('src','http://apps.bdimg.com/libs/jquery/'+jquery_version+'/jquery.min.js');
    // Add the script to the 'head' for processing
    document.getElementsByTagName('head')[0].appendChild(script);
    // Create a way to wait until script loading
    var attempts = 15;
    (function(){
      // Check again if jQuery is undefined
      if(typeof window.jQuery == 'undefined') {
        if(--attempts > 0) {
          // Calls himself in a few milliseconds
          window.setTimeout(arguments.callee, 250)
        } else {
          // Too much attempts to load, send error
          alert('An error ocurred while loading jQuery')
        }
      } else {
          bookmarklet();
      }
    })();
  }
})()