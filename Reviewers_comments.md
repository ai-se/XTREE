# Comments from the editors and reviewers

![image](https://cloud.githubusercontent.com/assets/1433964/20149973/8902ced6-a681-11e6-8ad2-3f796cb1807c.png)

### Editor

Dear Authors, 
The reviewers have finished evaluating your work. As you can observe, they raised some concerns that deserve your attention. It is important that you take into account their comments and evolve the paper accordingly. Please,  evolve the paper to make clear the defect model, hypothesis, limitations and readability and prepare a letter of changes explaining all modifications made. 


### Reviewer 1

- This paper presents the results of a case study regarding the likelihood that a code reorganization to address bad code smells will yield improvement in the defect proneness of the code. Five research questions were investigated and results pointed out that code modules that are changed in response to XTREE’s recommendations contain significantly fewer defects than recommendations from previous studies. Further, XTREE endorses changes to very few code metrics and the bad smell recommendations are not universal to all software projects.

This work provides useful insights to support the hard task to decide where to put efforts to reorganize code in software projects. This is an old problem in the software evolution area but that requires continuous investigation due to the new scenarios we face when developing software projects.

In overall, I enjoyed to read the paper and I think it is well structured. Despite this, some suggestions that I´d like to see incorporated in the paper are:

1- I missed a section discussing possible implications for researchers and practitioners. How the results of this work contribute to future research activities in the area? How can practitioners benefit from the results achieved in the paper?

2- I also missed a section presenting the main limitations of the work. Although some words have been said about it, I believe it is important to have a more structured discussion on a specific section.

3- It would be interesting to have further discussion at the end indicating how this work complements the body of knowledge about code smells (specifically, on the elimination of them in software projects). Do reached results indicate a similar direction? contradictory? Does This work somehow confirm the results of other studies or points to new directions?

Another point is: this work evaluated XTREE , a framework to evaluate whether a code reorganization is likely to have a perceivable benefit in terms of defect-proneness. It is fine to have this scope (defect-proneness) in terms of evaluation. However, it would be nice to have a discussion on why this characteristic (defect-proneness) is good to support the decision on code reorganization and/or how it could complement other characteristics. For instance, nowadays we are seeing a growing discussion on technical debt, that brings financial aspects (interest, principal, debt…) to the decision-making process on development activities. Could we use XTREE as a strategy to prioritize the payment of technical debt items?

Finally, I have one last question: is there any reason for do not use the GQM template to state the goal of the study and also to define null and alternative hypotheses for the research questions? 


- Reviewer 2

- This paper is about a tool that investigates a log of historical defects to suggest changes that will reorganize code to reduce the defect-proneness of the code. The motivation is that often code reorganization (refactoring) is carried out to remove code bad smells even though such smells do no increase the likelihood of defects in a given setting. That kind of reorganization would then be wasted effort. 

I sympathize with this approach. Software development is certainly dependent on many context factors. So learning the effect of various smells in a given context as input to how to deal with the smells is “intelligent”, as the title of the paper indicates.
However, the paper and thus its contributions are difficult to understand. For example, the introduction talks about Fowler’s bad smells and refers to literature on the (often contradictory) effects of such smells. And Figure 1 shows a list of bad smells. However, without making it clear, the paper continues to talk about smells but the real topic is not the smells but the metrics that are used to identify various smells. What’s the connection between whether a smell is bad or not and the threshold values of the various code metrics?

I also find it very difficult to understand the conceptual model of defects in this paper. The concept of “number of defects (defect counts)” is fully mixed with the concept of “percent of classes with defects/defective modules/ presence or absence of defects”. What does it then mean to “reduce defects in our data sets”? Is it the total number of defects in the data set (system?) or the number of “infected modules” in the data set? No examples illustrate this. How does a log of defects look like? What kind of information is recorded?

Furthermore, from RQ1: “This code reorganization will start with some initial code base that is changed to a new code base. For example, if the bad smell is loc > 100 and a code module has 500 lines of code, we reason optimistically that we can change that code metric to 100. Using the secondary verification oracle, we then predict the number of defects in new.” What is the idea here? Is the point that a log history of defects has shown that modules with more than 100 loc have more defects (per lines of code?) than smaller modules, and then the action is to reduce the size of that module? In case four new modules are developed, is there then also a log history that shows how the total number of modules in the system correlates with the total number of defects? Are we talking about total number of defects or only the number of “infected modules”?

My questions reveal that I’m not really into this stuff but I should be able to understand such a paper meant to be published in a generic software engineering journal. Unfortunately, I cannot accept the paper when I don’t understand what’s going on.

 

Other comments:
The RQs in the introduction are at a very low level. Actually, I wouldn’t call them research questions because they are too internal. RQ1 is  “which of the methods is most accurate?” without presenting the methods. They are just referred to in three other papers that probably describe them. What are your selection criteria for comparing the tool (or framework or system as you also call it) XTREE with exactly these methods? What’s the difference between tool, framework, and method in this paper? How does this work related to the work by Arcelli Fontana, in particular: Arcelli Fontana, F., Mäntylä, M.V., Zanoni, M. et al. Comparing and experimenting machine learning techniques for code smell detection, Empir Software Eng (2016) 21: 1143. doi:10.1007/s10664-015-9378-4?

 RQ5 is at a more general level. It is about the relationship between several code metrics. Improving on one metric may cause degradation on another one. This issue could have been much more spelled out with good examples in the paper. There is one example that reducing LOC may increase coupling (e.g. Efferent Coupling (EC). However, the way it’s formulated sounds odd to me. It’s stated that XTREE “recommends” (or “suggests”) increasing coupling while reducing LOC of a module. Sure, if you split a module into several smaller modules, or move code from one large module to other, smaller modules, usually the overall coupling will increase.  But isn’t that an avoidable consequence that will occur implicitly in the process of module splitting or moving code between modules? The way it’s formulated now gives the impression that the programmers should follow the recommendation of increasing the coupling, that is as if it’s a conscious action. Or am I missing the point?

For an outsider, it is difficult to follow the structure and argumentation of much of the paper. For example, in Section 4: “It can be difficult to judge the effects of removing bad smells. Code that is reorganized cannot be assessed just by a rerun of the test suite since such reorganizations may not change the system behavior (e.g., refactorings).” Isn’t the point about removing bad smells to improve the code without changing the behavior (refactorings)? Why cannot a test suite be run before and after if the behavior is not changed?

Figure 4 shows the effect of tuning, and the authors write: “The rows marked with a * in Figure 4 show data sets whose performance was improved remarkably  by  these  techniques. For example, in poi, the recall increased by 4% while the false alarm rate dropped by 21%.” This is a good example of researcher bias. Your example is the most favorable example from your point of view. It is one of only two of the eight data sets that improved on both pd and pf.

The authors state that if there are no historical records of defects, the results of this paper can be used as a guide (which results?). It is referred to Table 8 in the abstract but there is no Table 8. Is it meant to be Figure 8? In case, it’s very hard to understand how that figure could be used. Or is it Figure 1 as stated in the conclusion, but how that Figure 1 compensate for a lack of historical records?

Section 2 discusses the idea of why not just ask developers about the effect of code smells when the research literature is contradictory. I find it odd to believe that practitioners should be able to resolve inconsistencies in the research literature. As researchers, we should obviously investigate more into why the results are contradictory. The reason may be varying the quality of the research or varying contexts. For example, several papers state that there are more problems in software components with a large number of smells than components with a low number of smells. One should dismiss such research if the size of the components is not adjusted for. There are certainly more problems with larger components than smaller components given other properties the same. The authors agree that practitioners should not be expected resolve contradictions. My point is that it is so obvious that most of Section 2 should be deleted. Figure 1 as part of a related work section may remain.

It is stated that this paper reports a case study. I know that within the SW community is its common to use the term case study to denote just a demonstration of an example performed by the researchers. But in more mature disciplines, which we should aim to become a member of, “case study” has a certain meaning (e.g. Yin 2003). It would mean an evaluation in a real software development context. This notes the case here. See also the work by Runeson and Host 2009 on case studies in software engineering. Regarding case study, what kind of work remains before the proposed tool could be used by practitioners?
