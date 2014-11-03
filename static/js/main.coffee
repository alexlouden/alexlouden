$ ->
  # Scroll to links
  $('nav a').click (e) ->
    try
      href = e.target.href.split('#')[1]
      e.preventDefault()
      newtop = $('section.' + href).offset().top
      $("html, body").animate(scrollTop: newtop, 500)
    catch e
      return