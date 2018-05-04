; exercise No.2, 12-Assembly6.pdf
; compute value of the following series: f(n, x)=sigma (x^k/k!) for k from 1 o n
section .data
    n dq 5
    x dq 5.e0

section .text
    global _start

_start:
    push qword[n]
    push qword[x]
    call computeSigma

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

computeSigma:
    enter 8, 0
    mov rcx, [rbp+24]
    xor rax, rax
    fldz
    fld qword[rbp+16]
    fld1
    fld1
    fldz
    while:
        inc rax
        cmp rax, rcx
        jg done
        mov [rbp-8], rax
        fild qword[rbp-8]
        fmulp st2
        fld st2
        fmul st4
        fstp st3
        fld st2
        fdiv st2
        faddp st1
        jmp while
    done:
    leave
    ret 16
