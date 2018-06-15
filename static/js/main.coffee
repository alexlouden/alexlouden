throttle = (func, wait) ->
  timeout = undefined
  context = undefined
  args = undefined
  result = undefined
  previous = 0

  later = ->
    previous = Date.now
    timeout = null
    result = func.apply(context, args)
    if !timeout
      context = args = null
    return

  throttled = ->
    now = Date.now
    remaining = wait - (now - previous)
    context = this
    args = arguments
    if remaining <= 0 or remaining > wait
      if timeout
        clearTimeout timeout
        timeout = null
      previous = now
      result = func.apply(context, args)
      if !timeout
        context = args = null
    else if !timeout
      timeout = setTimeout(later, remaining)
    result

  throttled


sticky_header = ->
  $body = $('html')
  $window = $(window)
  fixed = false
  navheight = 115
  fixednavheight = 55 # + 100
  # 100 extra so that you're properly in the section before switching

  get_sections = ->
    sections = (
      {
        height: $(s).offset().top,
        section: $(s),
        nav: $('nav a[href="#'+$(s).attr('class')+'"]')
      } for s in $('section'))

  sections = get_sections()

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
    for s, i in sections by -1
      mid_browser = scrolltop + $window.height() / 2
      s_height = if i > 0 then s.height else 0
      if mid_browser >= s_height
        s.nav
          .addClass('active')
          .siblings().removeClass('active')
        return

  $(window).on 'resize scroll', throttle(onscroll, 20)
  $(window).on 'resize', throttle(get_sections, 100)

  onscroll()


on_nav_click = (e) ->
  try
    href = e.target.href.split('#')[1]
    e.preventDefault()
    newtop = $('section.' + href).offset().top
    newtop = 0 if newtop < 200
    $("html, body").animate(scrollTop: newtop, 500)
  catch e
    return

$ ->

  small_nav = $('nav').css('max-width') == "300px"

  if not small_nav
    sticky_header()

  $('nav a').on 'click', on_nav_click
