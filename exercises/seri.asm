; exercise No.2, 12-Assembly6.pdf
; compute value of the following series: f(n, x)=sigma (x^k/k!) for k from 1 o n
section .data
    n dq 10
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
    enter 32, 0
    mov rcx, [rbp+16]
    xor rax, rax
    while:
        inc rax
        cmp rax, rcx
        jg done
        mov [rbp-8], rax
        fild qword[rbp-8]
        fmulp qword[rbp-16]
        fld qword[rbp+24]
        fmulp qword[rbp-24]
        fldz
        fstp qword[rbp-8]
        fld qword[rbp-16]
        faddp qword[rbp-8]
        fld qword[rbp-24]
        fmulp qword[rbp-8]
        fld qword[rbp-8]
        faddp qword [rbp-32]
        jmp while
    done:
    leave
    ret 16
