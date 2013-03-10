-  the way to handle different platforms:
	- checker deduces platform type and each platform (win32, win64, lin, and so on) has separate job sequence
	

- Implement AGNENT GROUPS, they can handle several agent instances  

HAVE TO implement
- agent groups -- to handle several agent hosts (symbol downloader should be)


-------------- think about sequencing!!!
- how to represent tree
mover
checker
selector<field_name: dict(value1: tree, value2:tree, value3:tree, default = "")>

-------------------------- JOB SCHEDULLING
- load balancing algorithms
- persistence : introducing agents groups that works at the same backend.

Thoughts:
if backend dies, just don't assign new tasks, old tasks will be processed after recovering, 
or it can'be implemented kind of cleanup method to move tasks to another agent

-----------------------
AT the first step lets take simple randomizing alghorithm




LOAD BALANCING GOOD LINKS
http://en.wikipedia.org/wiki/Load_balancing_%28computing%29
http://en.wikipedia.org/wiki/Scheduling_algorithm
http://en.wikipedia.org/wiki/Round-robin_DNS

GOOD load balancing algorithms:
http://www2.cs.uni-paderborn.de/cs/ag-monien/RESEARCH/LOADBAL/
http://www2.cs.uni-paderborn.de/fachbereich/AG/monien/RESEARCH/LOADBAL/basics.html


---------------------------
Find the way to customizing alghorithms for infrastrocture 
