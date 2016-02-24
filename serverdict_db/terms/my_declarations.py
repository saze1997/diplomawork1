__author__ = 'Alexander Zelentsov'
import random
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import urllib.parse as urllib
from abc import abstractmethod

lipsum = ["Lorem ipsum dolor sit amet,"
          " consectetur adipiscing elit."
          " Suspendisse pellentesque,"
          " ligula in faucibus ultricies,"
          " nulla velit euismod ex,"
          " non venenatis ligula purus dictum ex.",
          " Vivamus quis arcu tempus ante scelerisque pretium."
          " Pellentesque et odio iaculis, interdum libero non,"
          " gravida quam. Suspendisse auctor purus vitae sapien cursus aliquet.",
          " Vestibulum a odio vitae arcu finibus condimentum eget vitae mauris."
          " Aenean nec tempor velit. In quis dictum turpis.",
          " Quisque sodales at neque a laoreet."
          " Suspendisse mollis mattis justo,"
          " vitae suscipit lacus luctus vel.",
          " Nulla sit amet congue arcu."
          " Aenean at leo ut urna dictum volutpat sed eget neque."
          " Etiam fringilla libero eu justo convallis interdum.",
          " Donec massa libero, euismod sit amet sem id,"
          " malesuada congue eros. Mauris malesuada commodo libero at finibus.",
          " Aenean mattis volutpat lorem, nec gravida tellus cursus nec."
          " Class aptent taciti sociosqu ad litora torquent per conubia nostra,"
          " per inceptos himenaeos. Donec eget urna id urna porta consectetur vel sed. "]

class Htmlable:
    @abstractmethod
    def get_html(self, request):
        pass


class NavigationItem(Htmlable):

    def __init__(self, text, active="",  href="#"):
        self.text, self.href, self.active = text, href, active

    def get_html(self, request=None):
        if request is not None:
            return get_template("navigation_item.html").render(RequestContext(request, {"item": self}))
        else:
            return get_template("navigation_item.html").render(Context({"item": self}))

    @staticmethod
    def get_html_for_menu(items):
        return get_template("navigation_items.html").render(Context({
            "navigation_items": [x.get_html for x in items]
        }, autoescape=False))

    @staticmethod
    def make_navigation(request, active_number=-1):
        items = [
            NavigationItem("Домой", href='/'),
            NavigationItem("О нас", href='about'),
            NavigationItem("Вход" if not request.user.is_authenticated() else "Выход",
                                           href="login"),
            NavigationItem("Поиск", href='search')
        ]
        if active_number != -1:
            items[active_number].active = 'active'
        return NavigationItem.get_html_for_menu(items)


class Article(Htmlable):

    def __init__(self, title="", content="", additional_info="", href="#"):
        self.title, self.href, self.content, self.additional_info = title, href, content, additional_info

    def get_html(self, request=None):
        if request is not None:
            return get_template("article.html").render(RequestContext(request, {"article": self}))
        else:
            return get_template("article.html").render(Context({"article": self}))


class Sidebar(Htmlable):

    def __init__(self, title, content, sidebar_type="middle-sidebar"):
        self.title, self.content, self.sidebar_type = title, content, sidebar_type

    def get_html(self, request=None):
        if request is not None:
            return get_template("sidebar.html").render(RequestContext(request, {"sidebar": self}))
        else:
            return get_template("sidebar.html").render(Context({"sidebar": self}))

    @staticmethod
    def get_random_sidebars(count: int):
        sidebars = ''
        sidebars = [Sidebar(
            "Боковая колонка №%i" % (x + 1),
            random.choice(lipsum)
        ) for x in range(count)]
        sidebars[0].sidebar_type = 'top-sidebar'
        sidebars[-1].sidebar_type = 'bottom-sidebar'
        r = ''.join([x.get_html() for x in sidebars])
        return r


class Message(Htmlable):
    def __init__(self, content):
        self.content = content

    def get_html(self, request=None):
        if request is not None:
            return get_template("message.html").render(RequestContext(request, {"message": self}))
        else:
            return get_template("message.html").render(Context({"message": self}))


def get_page(request, main_content='', sidebars='', nav_active_number=-1):
    return HttpResponse(
        get_template('index.html').render(RequestContext(request, {
            "Content": main_content,
            "Navigation": NavigationItem.make_navigation(request, nav_active_number),
            "Sidebars": sidebars})))


def get_error_page(msg=''):
    return HttpResponseRedirect('/error?message=%s' % (urllib.quote_plus(msg)))
