# A5 – Project Reflection

**Course:** 41934 Advanced BIM  
**Group:** STRU_26_20 – Structures  
**Project:** Building 308

## Introduction

Throughout the Advanced BIM course, our group has worked with OpenBIM, IFC models and Python to explore how BIM data can be used for automated structural analysis and model validation.

The assignments have gradually developed our understanding of IFC data, from extracting basic information to developing a tool for checking potential geometric load paths.

Our work is documented in the following assignments:

- [[A3 – Teach](../A3/README.md)](https://github.com/ViljaKristiansen/STRU_26_20/tree/main/A3): Tutorial on extracting BIM data using Python and IfcOpenShell.
- [[A4 – Tool](../A4/README.md)](https://github.com/ViljaKristiansen/STRU_26_20/tree/main/A4): IFC Load Path Checker for identifying potential geometric support paths between structural elements and foundation candidates.
- **A5 – Reflect:** Individual reflections and group evaluation of our learning experience.

---

## 1. Learning Experience

### June Muren Ertesvåg (s253445)

Before starting this course, I had a lot of experience with Revit and BIM modelling, but less experience with Python and working with IFC data. I would therefore say that I started at the Analyst level, but with limited experience in using Python for BIM analysis. Throughout the course, I have learned how Python and IfcOpenShell can be used to extract and analyse information from IFC models. In A1, we discovered that the information in an IFC model does not always match what is described in the structural report. In A2, we learned how to identify a specific problem and develop a workflow for checking it. In A3, we created a tutorial based on what we had learned about extracting IFC information with Python, which also helped me understand the basic code better. Through developing our Load Path Checker in A4, I learned more about how IFC geometry and information can be used to automate model checks. I would still place myself at the Analyst level, but with a much better understanding of how BIM data can be used beyond modelling. However, I still have a lot to learn when it comes to Python, especially understanding the code properly and being able to develop and improve it more independently.

### Vilja Kristiansen (s253442)

Before this course, i had basic knowledge to BIM, IFC and Python. I have previously used AI tools to help me write codes, but had little knowledge about the different parts to what the codes actually write. I could therefore make a script run without actually knowing or understanding how the results were made.
By the end of this course, i have become more confident in using VS code and how to extract information from IFC files by use of Python and IfcOpenShell. I can now better understand how to find different construction elements and extract information about them by their name and GlobalIds. Which as a result makes it easier to find elements in models and review the results from the script. I would still like to learn more and become more independent in writing and understanding codes.

---

## 2. Developing the Tutorial

Tutorial titled **Automating BIM Data Extraction with Python**.

For A3, we worked together to create a tutorial showing how Python and IfcOpenShell can be used to open an IFC model, identify and count structural columns, and extract information such as names and GlobalIds. The tutorial was based on techniques we had learned while developing our A4 tool. Our goal was to explain the basics of IFC data extraction in a way that students with limited Python experience could understand.

One of the challenges was teaching others how to use something we had limited experience with ourselves. We had to think carefully about which steps needed more explanation and how users could check that the code was working correctly. This also helped us understand the code and the process better.

We liked working with a use case that was relevant to structural engineering. However, clearer examples early in the course of how much a use case should cover would have helped us define the scope of our project. We also found it challenging to learn so many new tools at once. We would have preferred to spend more time learning VS Code and Blender, since these were the tools we used the most. The course has also given us ideas for how Python and OpenBIM could be used in our master's theses, especially for automating model checks and analysing structural information.

---

## 3. Group Reflection – Feedback and Tool Evaluation

### Feedback on the tutorial

We received very positive feedback on our A3 tutorial. The video was described as informative and easy to follow, especially because we combined all the steps into one video with a voiceover explaining the process. This made it easier for others to understand the code and follow along. The tutorial was also selected to be shown to the whole class and will also be available for future students to use as learning material through the video link in our A3 README. 

### Did the tool address the identified use case?

In A2, our group identified the need to check whether structural elements have a potential continuous geometric support path towards the foundation system.

To address this, we developed the **IFC Load Path Checker** in A4.

The tool uses Python and IfcOpenShell to analyse structural and geotechnical IFC models. It identifies potential geometric connections between slabs, beams, columns, walls and selected foundation candidates.

The tool generates JSON and CSV results, identifying elements with potential support paths and elements requiring further investigation.

The latest documented analysis included 800 structural elements and identified:

- 109 elements with potential paths and no unresolved branches.
- 339 elements with potential paths but unresolved branches.
- 242 elements with paths identified only when unverified geometric intersections were considered.
- 95 elements without an identified geometric path.
- 15 elements with insufficient geometry for the applied method.

These results demonstrate that the tool can identify potential geometric support paths and highlight elements requiring further review.

However, the tool performs geometric screening rather than structural verification. It does not assess structural capacity, connection resistance or actual load transfer.

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

The most important thing I learned from this course was how Python can be used to extract information from IFC models, since IFC is widely used in the construction industry. The most challenging part was the Python coding itself, especially figuring out how to develop a good tool that could also check its own results.

I am most satisfied with the fact that we managed to develop a useful tool and gained knowledge that we can take with us into our future careers. If I were to do something differently, I would probably narrow down the scope and focus on a more specific tool. Our tool became quite extensive, and since it cannot always identify the load paths correctly, manual inspection of the model is still necessary.

Overall, the course has given me a much better understanding of BIM and what it can be used for beyond modelling in Revit, creating IFC files and performing clash detection. I now see more possibilities for using BIM and Python in structural engineering, and this is something I will take with me into my future work.

### Vilja Kristiansen (s253442)

In A1, we compared information from the structural report with what we could fin in the IFC model. in A2, we turned that experience into a specific question about how structural elements are possibly supported. Creating the A3 tutorial helped me better understand the steps behind extracting IFC data, and in A4 we used that knowledge to build a tool that checks for possible support paths to the foundations.

Looking back, A4 made me think more carefully about what results from scripts actually tell me. For example, if the tool finds no support path for a beam, I would first look at the beam and the surrounding elements in the model. The result could point to a gap in the model or to a support condition that our method did not capture. This is where I see the value of automation in structural engineering, in addition to that it can help me decide where to look first and what to investigate in more detail
