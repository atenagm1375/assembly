; exercise No.2, 08-Assembly3.pdf
; write a program that says whether the number in rax is perfect or not.
section .data
    a dq 8128

section .text
    global _start

_start:
    mov rax, [a]
    call isPerfect

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

isPerfect:
    cmp rax, 1
    jle end
    mov r8, rax
    xor r9, r9                          ; result is stored in r9(if rax is perfect then r9=1 else r9=0)
    mov rcx, 1
    mov rbx, 2
    while:
        mov rax, r8
        xor rdx, rdx
        div rbx
        cmp dx, 0
        jne continue
        add rcx, rbx
        continue:
        inc rbx
        cmp rbx, r8
        jl while
    mov rbx, 1
    cmp rcx, r8
    cmovz r9, rbx
    end:
    ret
