const out = document.getElementById("out")
let c = 0

setInterval(function() {
    // allow 1px inaccuracy by adding 1
    const isScrolledToBottom = out.scrollHeight - out.clientHeight <= out.scrollTop + 1

    const newElement = document.createElement("div")

    //newElement.textContent = format(c++, 'Bottom position:', out.scrollHeight - out.clientHeight, out.scrollTop)

    out.appendChild(newElement)

    // scroll to bottom if isScrolledToBottom is true
    if (isScrolledToBottom) {
      out.scrollTop = out.scrollHeight - out.clientHeight
    }
}, 500)

function format () {
  return Array.prototype.slice.call(arguments).join(' ')
}