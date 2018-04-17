; exercise No.3, 10-assembly4.pdf
; write a program that does the multiplication using addition{al*bl=ah:al}
section .text
    global _start

_start:
    mov eax, -2000
    mov ebx, 19
    call multiplication

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

multiplication:
    xor r8, r8
    xor rcx, rcx
    cmp eax, 0
    cmove eax, ecx
    je end
    jl negative1
    check2:
    cmp ebx, 0
    cmove eax, ecx
    je end
    jl negative2
    continue:
    mov ecx, ebx
    mov rdx, rax
    dec ecx
    while:
        add rax, rdx
        loop while
    cmp r8, 1
    jne end
    neg rax
    end:
    ret

    negative1:
    neg eax
    inc r8
    jmp check2

    negative2:
    neg ebx
    inc r8
    jmp continue
