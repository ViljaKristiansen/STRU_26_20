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

### Student 1

*To be completed.*

### Student 2

*To be completed.*

---

## 2. Developing the Tutorial

For A3, our group developed a tutorial titled **Automating BIM Data Extraction with Python**.

The tutorial demonstrates how to use Python and IfcOpenShell to open an IFC model, identify structural columns, count the elements and extract information such as their names and GlobalIds.

The tutorial was based on techniques that were also relevant to developing our A4 tool. We wanted to explain the basic principles of IFC data extraction in a way that students with limited Python experience could follow.

*To be completed: Reflection on the choice of use case, course tools, freedom in the assignments and relevance for future thesis work.*

---

## 3. Group Reflection – Feedback and Tool Evaluation

### Feedback on the tutorial

*To be completed after reviewing peer feedback.*

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

### Student 1

I will most likely use OpenBIM in my master's thesis, and after this course I feel that I have a much better foundation for using it. I think these tools can be useful for automating tasks and making work more efficient. The course has also opened my eyes to more possibilities for what BIM can actually be used for, beyond just modelling.

I also expect to use OpenBIM in my future work as a structural engineer, since there is always a need to improve and make working methods more efficient. I think it will be especially useful for checking and validating models and results. I can also see myself using Python for different tasks, such as automating repetitive work, performing checks and extracting information from BIM models.

### Student 2

*To be completed.*

---

## 5. Individual Wrap-up

### Student 1

*To be completed.*

### Student 2

*To be completed.*
