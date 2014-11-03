

$ ->
  $body = $('body')
  fixed = false
  navheight = 115
  fixednavheight = 55

  sections = (
    {
      height: $(s).offset().top,
      section: $(s),
      nav: $('nav a[href=#'+$(s).attr('class')+']')
    } for s in $('section'))
  
  onscroll = (e) ->
    scrolltop = $body.scrollTop()

    # Sticky nav
    if not fixed and scrolltop > navheight 
      fixed = true
      $('header').addClass 'fixed'
    else if fixed and scrolltop <= navheight
      fixed = false
      $('header').removeClass 'fixed'

    # Underlining
    scrolltop += fixednavheight
    for s, i in sections
      next = sections[i + 1]
      if s.height <= scrolltop
        if not next or next and scrolltop < next.height
          s.nav
            .addClass('active')
            .siblings().removeClass('active')
      
  $(window).scroll onscroll

  # Scroll to links
  $('nav a').click (e) ->
    try
      href = e.target.href.split('#')[1]
      e.preventDefault()
      newtop = $('section.' + href).offset().top
      $("html, body").animate(scrollTop: newtop, 500)
    catch e
      return
