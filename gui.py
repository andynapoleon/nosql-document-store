import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import queries

class Library(tk.Tk):
    def __init__(self, *args, **kwargs):
        """
        Description: initialize
        Arguments: 
            None
        Return:
            None
        """
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in [User, Article, Author]:

            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.frames[User].tkraise()
        self.geometry("800x1080")
        self.title("Library database")

    def show_user(self):
        """
        Description: change between frames
        Arguments:
            cont: frame to change to
        Return:
            None
        """
        frame = self.frames[User]
        frame.update()
        frame.tkraise()

    def show_article(self, article):
        """
        Description: change frame to article
        Arguments:  
            pid: playlist id
        Return:
            None
        """
        frame = self.frames[Article]
        frame.article = article
        frame.update()
        frame.tkraise()

    def show_author(self, name):
        """
        Description: show frame profile of an author
        Arguments: 
            aid: artist id
        Return:
            None
        """
        frame = self.frames[Author]
        frame.name = name
        frame.update()
        frame.tkraise()

# main menu screen for user
class User(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: initialize frame
        Arguments:
            parent: parent of user frame
            controller: to swap between frames
        Return:
            None
        """
        tk.Frame.__init__(self,parent)
        
        self.controller = controller
        self.article_btn = []
        self.author_btn = []
        self.venue_btn = []
        self.entries = []
        self.article_page = 1
        self.author_page = 1
        self.venue_page = 1

        article_entry = ttk.Entry(self)
        self.entries.append(article_entry)
        article_search = ttk.Button(self, text = "search for articles", command= lambda :  self.get_articles(article_entry.get()))
        
        author_entry = ttk.Entry(self)
        self.entries.append(author_entry)
        author_search = ttk.Button(self, text = "search for authors", command= lambda :  self.get_authors(author_entry.get()))
        
        venue_entry = ttk.Entry(self)
        self.entries.append(venue_entry)
        venue_search = ttk.Button(self, text = "list venues", command= lambda :  self.get_venues(venue_entry.get()))

        add_label = ttk.Label(self, text = "Add an article here")

        id_label = ttk.Label(self, text = "Unique ID")
        id_entry = ttk.Entry(self)
        self.entries.append(id_entry)

        title_label = ttk.Label(self, text = "Title")
        title_entry = ttk.Entry(self)
        self.entries.append(title_entry)

        authors_label = ttk.Label(self, text = "Authors (separated by commas)")
        authors_entry = ttk.Entry(self)
        self.entries.append(authors_entry)

        year_label = ttk.Label(self, text = "Year")
        year_entry = ttk.Entry(self)
        self.entries.append(year_entry)

        add_btn = ttk.Button(self, text = "Add article", command= lambda :  self.add_article(id_entry.get(),title_entry.get(),authors_entry.get(),year_entry.get()))

        article_entry.grid(row = 0, column = 0)
        article_search.grid(row = 0, column = 1)

        author_entry.grid(row = 10, column = 0)
        author_search.grid(row = 10, column = 1)

        venue_entry.grid(row = 20, column = 0)
        venue_search.grid(row = 20, column = 1)

        add_label.grid(row = 30, column = 0)

        id_label.grid(row = 40, column = 0)
        id_entry.grid(row = 40, column = 1)

        title_label.grid(row = 50, column = 0)
        title_entry.grid(row = 50, column = 1)

        authors_label.grid(row = 60, column = 0)
        authors_entry.grid(row = 60, column = 1)

        year_label.grid(row = 70, column = 0)
        year_entry.grid(row = 70, column = 1)

        add_btn.grid(row = 80, column = 1)
        
        self.article_page_entry = ttk.Entry(self)
        self.article_page_btn = ttk.Button(self, text = "Go", command = lambda: self.article_npage(self.article_page_entry.get()))
        self.article_page_lbl = ttk.Label(self, text = "Currently in page 1")
        self.entries.append(self.article_page_entry)

        self.article_page_entry.grid(row = 6, column = 0)
        self.article_page_btn.grid(row = 6, column = 1)
        self.article_page_lbl.grid(row = 7, column = 1)

        self.author_page_entry = ttk.Entry(self)
        self.author_page_btn = ttk.Button(self, text = "Go", command = lambda: self.author_npage(self.author_page_entry.get()))
        self.author_page_lbl = ttk.Label(self, text = "Currently in page 1")
        self.entries.append(self.author_page_entry)

        self.author_page_entry.grid(row = 16, column = 0)
        self.author_page_btn.grid(row = 16, column = 1)
        self.author_page_lbl.grid(row = 17, column = 1)

        self.venue_page_entry = ttk.Entry(self)
        self.venue_page_btn = ttk.Button(self, text = "Go", command = lambda: self.venue_npage(self.venue_page_entry.get()))
        self.venue_page_lbl = ttk.Label(self, text = "Currently in page 1")
        self.entries.append(self.venue_page_entry)

        self.venue_page_entry.grid(row = 26, column = 0)
        self.venue_page_btn.grid(row = 26, column = 1)
        self.venue_page_lbl.grid(row = 27, column = 1)

    # question 4
    def add_article(self,aid,title,authors,year):
        # check conditions of parameters
        authors = authors.split(",")
        try:
            year= int(year)
        except:
            messagebox.showinfo("Alert","Enter a valid year")
            return
        # aid unique (no aid existed already)
        if queries.check_exists(aid):
            messagebox.showinfo("Alert","ID already existed")
            return
        queries.add_article(aid,title,authors,str(year))
        messagebox.showinfo("Alert","Article added successfully")
        # raise messagebox if aid not unique

    # question 1
    def get_articles(self, keywords):
        #querying
        self.articles = list(queries.find_articles(keywords))
        self.article_page = 1
        self.display_articles()
        
    def display_articles(self):
        self.article_page_lbl.config(text = "currently in page " + str(self.article_page))
        for btn in self.article_btn:
            btn.destroy()
        if self.articles == []:
            return
        iteration = 5
        if self.article_page == len(self.articles) // 5 +1:
            if len(self.articles) % 5 != 0:
                iteration = len(self.articles) % 5
        for i in range (iteration):
            button = ttk.Button(self, text = "id: " + self.articles[(self.article_page-1)*5+i]["id"] + "\n"
            + "title: " + self.articles[(self.article_page-1)*5+i]["title"] + "\n"
            + "year: " + self.articles[(self.article_page-1)*5+i]["year"] + "\n"
            + "venue: " + self.articles[(self.article_page-1)*5+i]["venue"],
            command = lambda x= self.articles[(self.article_page-1)*5+i]: self.controller.show_article(x))
            button.grid(row = 1+i, column = 1)
            self.article_btn.append(button)

    def article_npage(self, pageno):
        try:
            self.article_page = int(pageno)
            if self.article_page <= 0 and self.article_page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number")
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.article_page > math.ceil(len(self.articles)/5):
            messagebox.showinfo("Alert","No more results")
            return
        self.display_articles()

    # question 2
    def get_authors(self, keyword):
        #check keywords
        if keyword.count(" ") != 0:
            #raise error
            messagebox.showinfo("Alert","Only one keyword allowed")
            return
        #querying
        self.authors = list(queries.find_authors(keyword))
        self.author_page = 1
        self.display_authors()
        
    def display_authors(self):
        self.author_page_lbl.config(text = "currently in page " + str(self.author_page))
        for btn in self.author_btn:
            btn.destroy()
        if self.authors == []:
            return
        iteration = 5
        if self.author_page == len(self.authors) // 5 +1:
            if len(self.authors) % 5 != 0:
                iteration = len(self.authors) % 5
        for i in range (iteration):
            button = ttk.Button(self, text = "name: " + self.authors[(self.author_page-1)*5+i]["_id"] 
            + ", number of articles: " + str(self.authors[(self.author_page-1)*5+i]["count"]), 
            command = lambda x= self.authors[(self.author_page-1)*5+i]["_id"]: self.controller.show_author(x))
            button.grid(row = 11+i, column = 1)
            self.author_btn.append(button)

    def author_npage(self, pageno):
        try:
            self.author_page = int(pageno)
            if self.author_page <= 0 and self.author_page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number")
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.author_page > math.ceil(len(self.authors)/5):
            messagebox.showinfo("Alert","No more results")
            return
        self.display_authors()
    
    # question 3
    def get_venues(self, number):
        try:
            number = int(number)
        except:
            messagebox.showinfo("Alert","Enter an integer")
        
        #querying
        self.venues = list(queries.find_top_venues(number))
        self.venue_page = 1
        self.display_venues()

    def display_venues(self):
        self.venue_page_lbl.config(text = "currently in page " + str(self.venue_page))
        for btn in self.venue_btn:
            btn.destroy()
        if self.venues == []:
            return
        iteration = 5
        if self.venue_page == len(self.venues) // 5 +1:
            if len(self.venues) % 5 != 0:
                iteration = len(self.venues) % 5
        for i in range (iteration):
            button = ttk.Label(self, text = "venue: " + self.venues[(self.venue_page-1)*5+i]["venue"] 
            + ", article count: " + str(self.venues[(self.venue_page-1)*5+i]["article_count"]) 
            + ", reference count: " + str(self.venues[(self.venue_page-1)*5+i]["rcount"]) 
            ,wraplength = 1500, anchor="center")
            button.grid(row = 21+i, column = 1)
            self.venue_btn.append(button)

    def venue_npage(self, pageno):
        try:
            self.venue_page = int(pageno)
            if self.venue_page <= 0 and self.venue_page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number")
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.venue_page > math.ceil(len(self.venues)/5):
            messagebox.showinfo("Alert","No more results")
            return
        self.display_venues()

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        for btn in self.article_btn:
            btn.destroy()
        for btn in self.author_btn:
            btn.destroy()
        for btn in self.venue_btn:
            btn.destroy()
        self.article_btn = []
        self.author_btn = []
        self.venue_btn = []
        self.article_page = 1
        self.author_page = 1
        self.venue_page = 1
        self.article_page_lbl.config(text = "currently in page " + str(self.article_page))
        self.author_page_lbl.config(text = "currently in page " + str(self.author_page))
        self.venue_page_lbl.config(text = "currently in page " + str(self.venue_page))
        for entry in self.entries:
            entry.delete(0,len(entry.get()))
        
    
class Article(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: initialize frame
        Arguments:
            parent: parent of user frame
            controller: to swap between frames
        Return:
            None
        """
        tk.Frame.__init__(self,parent)
        self.article = {}
        self.ref_page = 1
        self.ref_btn = []

        self.id_lbl = ttk.Label(self,text="",wraplength=1500, anchor="center")
        self.title_lbl = ttk.Label(self,text="",wraplength=1500, anchor="center")
        self.year_lbl = ttk.Label(self,text="",wraplength=1500, anchor="center")
        self.venue_lbl = ttk.Label(self,text="",wraplength=1500, anchor="center")
        self.abstract_lbl = ttk.Label(self,text="",wraplength = 1500, anchor="center")
        self.authors_lbl = ttk.Label(self,text="",wraplength=1500, anchor="center")

        self.references_lbl = ttk.Label(self, text = "Referenced by: ")
        self.ref_page_entry = ttk.Entry(self)
        self.ref_page_btn = ttk.Button(self, text = "Go", command = lambda: self.ref_npage(self.ref_page_entry.get()))
        self.ref_page_lbl = ttk.Label(self, text = "Currently in page 1")
        self.home_btn = ttk.Button(self, text = "Main Menu", command = lambda: controller.show_user())

        self.id_lbl.grid(row = 40, column = 0)
        self.title_lbl.grid(row = 41, column = 0)
        self.year_lbl.grid(row = 42, column = 0)
        self.venue_lbl.grid(row = 43, column = 0)
        self.abstract_lbl.grid(row = 45, column = 0)
        self.authors_lbl.grid(row = 44, column = 0)

        self.references_lbl.grid(row = 6, column = 0)
        self.ref_page_entry.grid(row = 26, column = 0)
        self.ref_page_btn.grid(row = 26, column = 1)
        self.ref_page_lbl.grid(row = 27, column = 1)
        self.home_btn.grid(row = 30,column = 0)

    def display_refs(self):
        self.ref_page_lbl.config(text = "currently in page " + str(self.ref_page))
        for btn in self.ref_btn:
            btn.destroy()
        if self.refs == []:
            return
        iteration = 5
        if self.ref_page == len(self.refs) // 5 +1:
            if len(self.refs) % 5 != 0:
                iteration = len(self.refs) % 5
        for i in range (iteration):
            button = ttk.Label(self, text = "id: " + self.refs[(self.ref_page-1)*5+i]["id"] + "\n"
            + "title: " + self.refs[(self.ref_page-1)*5+i]["title"] + "\n"
            + "year: " + self.refs[(self.ref_page-1)*5+i]["year"] 
            ,wraplength = 1500, anchor="center")
            button.grid(row = 21+i, column = 0)
            self.ref_btn.append(button)

    def ref_npage(self, pageno):
        try:
            self.ref_page = int(pageno)
            if self.ref_page <= 0 and self.ref_page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number")
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.ref_page > math.ceil(len(self.refs)/5):
            messagebox.showinfo("Alert","No more results")
            return
        self.display_refs()

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        self.ref_page = 1
        if "id" in self.article:
            self.id_lbl.config(text="id: " + self.article["id"], anchor="center")
        if "title" in self.article:
            self.title_lbl.config(text= "title: " +  self.article["title"], anchor="center")
        if "year" in self.article:
            self.year_lbl.config(text="year: " + self.article["year"], anchor="center")
        if "venue" in self.article:
            self.venue_lbl.config(text="venue: " + self.article["venue"], anchor="center")
        if "abstract" in self.article:
            self.abstract_lbl.config(text="abstract: " + self.article["abstract"], anchor="center")
        if "authors" in self.article:
            self.authors_lbl.config(text="authors: " + ",".join(self.article["authors"]), anchor="center")
        self.refs = list(queries.find_references(self.article["id"]))
        self.ref_page_entry.delete(0,len(self.ref_page_entry.get()))
        self.display_refs()

class Author(tk.Frame):
    def __init__(self, parent, controller):
        """
        Description: initialize frame
        Arguments:
            parent: parent of user frame
            controller: to swap between frames
        Return:
            None
        """
        tk.Frame.__init__(self,parent)
        self.name = ''
        self.aut_page = 1
        self.aut_btn = []
        self.auts_lbl = ttk.Label(self, text = "Articles by this author: ")
        self.aut_page_entry = ttk.Entry(self)
        self.aut_page_btn = ttk.Button(self, text = "Go", command = lambda: self.aut_npage(self.aut_page_entry.get()))
        self.aut_page_lbl = ttk.Label(self, text = "Currently in page 1")
        self.home_btn = ttk.Button(self, text = "Main Menu", command = lambda: controller.show_user())

        self.auts_lbl.grid(row = 0, column = 0)
        self.aut_page_entry.grid(row = 6, column = 0)
        self.aut_page_btn.grid(row = 7, column = 1)
        self.aut_page_lbl.grid(row = 8, column = 1)
        self.home_btn.grid(row = 9,column = 0)

    def display_auts(self):
        self.aut_page_lbl.config(text = "currently in page " + str(self.aut_page))
        for btn in self.aut_btn:
            btn.destroy()
        if self.auts == []:
            return
        iteration = 5
        if self.aut_page == len(self.auts) // 5 +1:
            if len(self.auts) % 5 != 0:
                iteration = len(self.auts) % 5
        for i in range (iteration):
            button = ttk.Label(self, text = "title: " + self.auts[(self.aut_page-1)*5+i]["title"] + "\n"
            + "year: " + self.auts[(self.aut_page-1)*5+i]["year"] + "\n"
            + "venue: " + self.auts[(self.aut_page-1)*5+i]["venue"]
            ,wraplength = 1500, anchor="center")
            button.grid(row = 1 + i, column = 0)
            self.aut_btn.append(button)

    def aut_npage(self, pageno):
        try:
            self.aut_page = int(pageno)
            if self.aut_page <= 0 and self.aut_page == float(pageno):
                messagebox.showinfo("Alert","You should type in a positive number")
        except:
            messagebox.showinfo("Alert","You should type in a number")
            return
        if self.aut_page > math.ceil(len(self.auts)/5):
            messagebox.showinfo("Alert","No more results")
            return
        self.display_auts()

    def update(self):
        """
        Description: update frame
        Arguments:
            None
        Return:
            None
        """
        self.aut_page = 1
        self.auts = list(queries.find_article_based_on_authors(self.name))
        self.aut_page_entry.delete(0,len(self.aut_page_entry.get()))
        self.display_auts()


    
