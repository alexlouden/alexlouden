throttle = (func, wait, options) ->
  timeout = undefined
  context = undefined
  args = undefined
  result = undefined
  previous = 0
  if !options
    options = {}

  later = ->
    previous = if options.leading == false then 0 else Date.now
    timeout = null
    result = func.apply(context, args)
    if !timeout
      context = args = null
    return

  throttled = ->
    now = Date.now
    if !previous and options.leading == false
      previous = now
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
    else if !timeout and options.trailing != false
      timeout = setTimeout(later, remaining)
    result

  throttled.cancel = ->
    clearTimeout timeout
    previous = 0
    timeout = context = args = null
    return

  throttled


sticky_header = ->
  $body = $('html')
  fixed = false
  navheight = 115
  fixednavheight = 55 # + 100
  # 100 extra so that you're properly in the section before switching

  sections = (
    {
      height: $(s).offset().top,
      section: $(s),
      nav: $('nav a[href="#'+$(s).attr('class')+'"]')
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

  $(window).on 'resize scroll', throttle(onscroll, 20)
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
