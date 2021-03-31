/*
  Slidemenu
*/
(function() {

    window.onload = function get_body() {
    var $body = document.getElementsByTagName('body')[0];
    var $menu_trigger = $body.getElementsByClassName('menu-trigger')[0];
    //console.log("from window on load:");
    //console.log($body);
    if ( typeof $menu_trigger !== 'undefined' ) {
		$menu_trigger.addEventListener('click', function() {
			$body.className = ( $body.className == 'menu-active' )? '' : 'menu-active';
		    });
	    }
    }
}).call(this);