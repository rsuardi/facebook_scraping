import gtk
import webkit

window = gtk.Window()
view = webkit.WebView()
view.open('http://www.google.com')
window.add(view)
window.show_all()
window.connect('delete-event', lambda window, event: gtk.main_quit())

gtk.main()