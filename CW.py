import tkinter as tk
from tkinter import scrolledtext
from tkinter import END
from tkinter import messagebox
import pickle
from sklearn import cluster
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Create search window
window = tk.Tk()
window.title('Welcome to Search Engin')
window.geometry('800x600')

# Set window size, add picture, set picture position
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='welcom.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# Create search input box
tk.Label(window, text='Search: ', font=('Arial', 24)).place(x=50, y=150)

keywords = tk.StringVar()
keywords.set('eg. artificial')
entry_keywords = tk.Entry(window, textvariable=keywords, font=('Arial', 16), width=50)
entry_keywords.place(x=160, y=155)

# Create a fuzzy search keyword prompt box
text = ("Fuzzy search input criteria:",
        "*****0***** -> Computer Science",
        "*****1***** -> Software Engineering",
        "*****2***** -> Deep Learning",
        "*****3***** -> Computer vision",
        "*****4***** -> Machine learning")
fuzzy = tk.StringVar()
fuzzy.set(text)
lb = tk.Listbox(window, width=25, height=6, listvariable=fuzzy)
lb.place(x=255, y=260)


# Inverted index, keyword search
def keywords_info():
    # Create a keyword index result display box
    window_result = tk.Toplevel(window)
    window_result.geometry('1000x800')
    window_result.title('Keywords Result')

    with open('result.pickle', 'rb') as file:
        info_set = pickle.load(file)

    # Word segmentation of documents, Get the word vector collection of the document
    all_words = []
    for i in info_set.values():
        cut = i.split()
        all_words.extend(cut)

    set_all_words = set(all_words)

    # Build an inverted index
    invert_index = dict()
    for j in set_all_words:
        temp = []
        for k in info_set.keys():
            filed = info_set[k]
            split_filed = filed.split()
            if j in split_filed:
                temp.append(k)
            invert_index[j] = temp

    search_info = keywords.get()

    # Set up search results display structure
    if search_info in invert_index.keys():
        prof_name = invert_index[search_info]
        res_name = []
        res_info = []
        for h in prof_name:
            res_name.append(h)
            for n in list(info_set.keys()):
                if n == h:
                    res_info.append(info_set[h])
        res = ''
        for m, n in zip(res_name, res_info):
            res = res + "Professor: {0}\nIntroduction: {1}\n" \
                        "******************************************************************************\n".format(m, n)
        scr = scrolledtext.ScrolledText(window_result, width=100, height=40, font=('Arial', 16))
        scr.place(x=20, y=25)
        scr.insert(END, res)

    elif search_info in info_set.keys():
        res_name = str(search_info)
        res_info = info_set[search_info]
        res = "Professor: {0}\nIntroduction: {1}\n" \
              "******************************************************************************\n".format(res_name, res_info)
        scr = scrolledtext.ScrolledText(window_result, width=100, height=40, font=('Arial', 16))
        scr.place(x=20, y=25)
        scr.insert(END, res)

    else:
        tk.messagebox.showerror('Error', 'Sorry, No content or information that matches your query!')
        res = 'Sorry, No content or information that matches your query!'
        scr = scrolledtext.ScrolledText(window_result, width=100, height=40, font=('Arial', 16))
        scr.place(x=20, y=25)
        scr.insert(END, res)


# Create fuzzy search function
def fuzzy_info():
    # Create a fuzzy search result display interface
    window_fuzzy = tk.Toplevel(window)
    window_fuzzy.geometry('1000x800')
    window_fuzzy.title('Fuzzy Result')

    with open('result.pickle', 'rb') as file:
        info_set = pickle.load(file)

    word_list = []
    for i in info_set.values():
        word_list.append(i)

    # Use Scikit-Learn calculate TF-IDF
    # Convert words in text to word frequency matrix
    vectorizer = CountVectorizer()
    # Count the number of occurrences of each word
    X = vectorizer.fit_transform(word_list)

    transformer = TfidfTransformer()
    # Count word frequency matrix X into TF-IDF value
    tfidf = transformer.fit_transform(X)
    tfidf_train = tfidf.toarray()
    # Use Scikit-Learn to perform K-means cluster analysis on documents.
    km = cluster.KMeans(n_clusters=5, random_state=100, max_iter=500)
    c = km.fit(tfidf_train)
    t = c.labels_

    # Display the clustered results
    info = ''
    for j, k in zip(t, list(info_set.values())):
        info = info + "*****{0}*****   {1}#".format(j, k)

    info_list = []
    info_list = info.split("#")

    for m, n in zip(info_set.keys(), info_list):
        info_set[m] = n

    search_info = keywords.get()

    pro_name = []
    pro_info = []

    for p, q in zip(list(info_set.keys()), list(info_set.values())):
        if search_info in q:
            pro_name.append(p)
            pro_info.append(q)

    res_1 = ''
    for l, k in zip(pro_name, pro_info):
        res_1 = res_1 + "Professor: {0}\nType: {1}\nIntroduction: {2}\n" \
                        "******************************************************************************\n".format(l, k[:11], k[11:])
    scr = scrolledtext.ScrolledText(window_fuzzy, width=100, height=40, font=('Arial', 16))
    scr.place(x=20, y=25)
    scr.insert(END, res_1)


# Set the function of the two buttons on the main search interface
btn_keywords = tk.Button(window, text='Keyword Search', font=('Arial', 16), command=keywords_info)
btn_keywords.place(x=200, y=210)
btn_fuzzy = tk.Button(window, text='Fuzzy Search', font=('Arial', 16), command=fuzzy_info)
btn_fuzzy.place(x=400, y=210)

window.mainloop()