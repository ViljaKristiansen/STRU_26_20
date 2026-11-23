# A5 – Project Reflection

**Course:** 41934 Advanced BIM  
**Group:** STRU_26_20 – Structures  
**Project:** Building 308

## Introduction

Throughout the Advanced BIM course, we have explored how Python and OpenBIM can be used to extract information from IFC models and automate structural model checks. Our work developed from basic IFC data extraction to creating a tool for identifying potential geometric load paths.

Our work is documented in the following assignments:

- [[A3 – Teach](../A3/README.md)](https://github.com/ViljaKristiansen/STRU_26_20/tree/main/A3): Tutorial on extracting BIM data using Python and IfcOpenShell.
- [[A4 – Tool](../A4/README.md)](https://github.com/ViljaKristiansen/STRU_26_20/tree/main/A4): IFC Load Path Checker for identifying potential geometric support paths between structural elements and foundation candidates.
- **A5 – Reflect:** Individual reflections and group evaluation of our learning experience.

---

## 1. Learning Experience

### June Muren Ertesvåg (s253445)

Before starting this course, I had a lot of experience with Revit and BIM modelling, but less experience with Python and working with IFC data. I would therefore say that I started at the Analyst level, but with limited experience in using Python for BIM analysis. Throughout the course, I have learned how Python and IfcOpenShell can be used to extract and analyse information from IFC models. In A1, we discovered the importance of understanding how information is represented in IFC models. In A2, we developed a use case for checking potential load paths, which we later used to create our A4 tool. Developing the A3 tutorial also helped me understand the basic Python code better. I would still place myself at the Analyst level, but with a much better understanding of how BIM data can be used beyond modelling. I still have a lot to learn about Python, especially understanding and developing code more independently.

### Vilja Kristiansen (s253442)

Before this course, i had experience in using BIM tools such as Revit, but minimal experience and knowledge to IFC and Python. I have previously used AI tools to help me write codes, but had little knowledge about the different parts to what the codes actually write. I could therefore make a script run without actually knowing or understanding how the results were made.
By the end of this course, i have become more confident in using VS code and how to extract information from IFC files by use of Python and IfcOpenShell. I can now better understand how to find different construction elements and extract information about them by their name and GlobalIds. Which as a result makes it easier to find elements in models and review the results from the script. I would still like to learn more and become more independent in writing and understanding codes.

---

## 2. Developing the Tutorial

For A3, we developed a tutorial titled Automating BIM Data Extraction with Python, based on techniques we had learned while developing our A4 tool. We demonstrated how to open an IFC model, identify and count structural columns, and extract information such as names and GlobalIds. Our goal was to make the process easy to follow for students with limited Python experience.

One challenge was teaching others something we had limited experience with ourselves. We had to consider which steps needed more explanation and how users could check that the code was working correctly. This also helped us understand the code better.

We liked working with a use case relevant to structural engineering, but clearer examples early in the course would have helped us define the scope of our project. We also found it challenging to learn so many new tools and would have preferred more time working with VS Code and Blender. The course has also given us ideas for using Python and OpenBIM in our master's theses, especially for automated model checking.

---

## 3. Group Reflection – Feedback and Tool Evaluation

### Feedback on the tutorial

We received very positive feedback on our A3 tutorial. The video was described as informative and easy to follow, especially because we combined all the steps into one video with a voiceover explaining the process. This made it easier for others to understand the code and follow along. The tutorial was also selected to be shown to the whole class and will also be available for future students to use as learning material through the video link in our A3 README. 

### Did the tool address the identified use case?

In A2, we identified the need to check whether structural elements have a potential continuous geometric support path towards the foundation system. To address this, we developed the IFC Load Path Checker in A4. The tool uses Python and IfcOpenShell to analyse structural and GEO IFC models and identify potential connections between structural elements. In our latest analysis of 800 structural elements, 448 had potential paths, including 339 with unresolved branches. Another 242 required consideration of unverified geometric intersections, while 95 had no identified path and 15 had insufficient geometry.

The tool partly addressed our use case by identifying potential support paths and highlighting elements that require further investigation. However, it cannot verify actual load transfer or structural capacity, and some results still require manual inspection of the model. We therefore see it as a useful screening tool rather than a complete load path verification tool.

### Relevant Advanced Building Design stages

The tool is primarily relevant during **Stages C and D**, when structural models contain sufficient detail for checking geometric relationships between structural elements.

It may support structural engineers and BIM coordinators by identifying potential modelling and coordination issues before further detailing and engineering review.

---

## 4. Future Use of OpenBIM

### June Muren Ertesvåg (s253445)

I will most likely use OpenBIM in my master's thesis, and after this course I feel that I have a much better foundation for using it. I think these tools can be useful for automating tasks and making work more efficient. The course has also opened my eyes to more possibilities for what BIM can actually be used for, beyond just modelling.

I also expect to use OpenBIM in my future work as a structural engineer, since there is always a need to improve and make working methods more efficient. I think it will be especially useful for checking and validating models and results. I can also see myself using Python for different tasks, such as automating repetitive work, performing checks and extracting information from BIM models.

### Vilja Kristiansen (s253442)

I would like to use OpenBIM in my master thesis, if it suits my topic. 
In my future work as a structural engineer I can see how OpenBIM could be of use, especially considering model checking and coordination between disciplines. For example, a script could flag elements that need a closer look before the model is used for further design work.

---

## 5. Individual Wrap-up

### June Muren Ertesvåg (s253445)

The most important thing I learned from this course was how Python can be used to extract information from IFC models, since IFC is widely used in the construction industry. The most challenging part was the Python coding itself, especially figuring out how to develop a good tool that could also check its own results. I am most satisfied with the fact that we managed to develop a useful tool and gained knowledge that we can take with us into our future careers. If I were to do something differently, I would probably narrow down the scope and focus on a more specific tool. Our tool became quite extensive, and since it cannot always identify the load paths correctly, manual inspection of the model is still necessary.

Overall, the course has given me a much better understanding of BIM and what it can be used for beyond modelling in Revit, creating IFC files and performing clash detection. I now see more possibilities for using BIM and Python in structural engineering, and this is something I will take with me into my future work.

### Vilja Kristiansen (s253442)

In A1, we compared information from the structural report with what we could fin in the IFC model. in A2, we turned that experience into a specific question about how structural elements are possibly supported. Creating the A3 tutorial helped me better understand the steps behind extracting IFC data, and in A4 we used that knowledge to build a tool that checks for possible support paths to the foundations.

Looking back, A4 made me think more carefully about what results from scripts actually tell me. For example, if the tool finds no support path for a beam, I would first look at the beam and the surrounding elements in the model. The result could point to a gap in the model or to a support condition that our method did not capture. This is where I see the value of automation in structural engineering, in addition to that it can help me decide where to look first and what to investigate in more detail
