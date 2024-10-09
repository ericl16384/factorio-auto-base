# cpu cycle

## legend
```
pulse   1 tick signal
extend  1 tick signal then stored in a register

start   first tick of stable signal
end     last tick of stable signal

change  change of stable signal
```

## timetable (not finished)
```
1       trigger pc      pulse   store

2       rom     opcode  pulse   filter
2       rom     writea  extend  ram
2       rom     ina     extend  alu
2       rom     inb     extend  alu   
2       rom     reada   pulse   ram
2       rom     readb   pulse   ram

3       alu     outa    start   mux
3       ram     ina     change  alu
3       ram     inb     change  alu
3       time    reset   pulse   ram
3       filter  opcode  extend  mux

...

4       alu     outa    change  mux
4       mux     opcode  start   ram
4       mux     outa    start   ram
4       time    reset   end     ram

5       mux     outa    change  ram
```

## systems
```
counter in  (pc)
counter out (pc, ...)

rom in      (*, pc)
rom out     (*, opcode, writea, reada, readb, ina, inb)

CHANGE NEEDED
reada in    (reada)
reada out   (data)

CHANGE NEEDED
readb in    (readb)
readb out   (data)

alu in      (ina, inb)
alu out     (ina)

CHANGE NEEDED
mux in      (opcode, outa)
mux out     (outa)

CREATION NEEDED
atob in     (ina)
atob out    (inb)

writea in   (*, writea, ina, inb)
writea val  (*, writea, ina, inb, ...)
```
