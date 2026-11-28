# Learned segmentation and neighboring mechanisms

**FB1.** Which measurements does ByteFlow's Table 3 compare across trained chunkers, and how many runs are averaged? Can those measurements establish whether the same segmentation rule preserves meaning on a new language?

**FB2.** A team wants to use ByteFlow where the top-ranked boundary slot moves between packets of the same length. Explain what the method fixes and what can vary with input. What should the team check before using the boundary decisions for a literal controller field?

**FB3.** In H-Net, what controls the pressure to make fewer chunks, and what paths bring the shortened stream back to byte resolution? What serving measurements should decide adoption if a batch runs late after internal sequence length shrinks?

**FB4.** The chapter compares a text JEPA's alignment with models much larger in parameter count. Give the sizes reported, distinguish the identity-predictor theorem from the practical run, and say what the result leaves open about replacing a text-generating specialist.
