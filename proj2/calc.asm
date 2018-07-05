; Ashena G.Mohammadi, 610394128
; calculator with the simple arithmetic functions-summation, multiplication,
; division, and subtraction-for both integers and floating point numbers

;******************************************************************************
;******************************************************************************

section .data
    msg db "Enter a valid operation or q to exit:", 10
    msg_len equ $-msg
    errormsg db "Illegal operation. Please, try again.", 10
    error_len equ $-errormsg
    divide_by_zero db "divide by zero", 10
    div_len equ $-divide_by_zero

    termios times 36 db 0
    stdin equ 0
    ICANON equ 1<<1
    ECHO equ 1<<3
    sys_read equ 3

    max_size equ 15
    calc_flag db 0

;******************************************************************************

section .bss
    num resq max_size       ; keeps a number
    op resb max_size        ; keeps operator
    inp resb 1              ; holds input char

;******************************************************************************

section .text
    global _start

_start:
    call canonical_off
    call evaluate_expression

;------------------------------------------------------------------------------

exit:
    call canonical_on
    mov rax, 1
    mov rbx, 0
    int 80h

;------------------------------------------------------------------------------

evaluate_expression:
    read_loop:
        call read_char
        call evaluate_char
        jmp read_loop

;..............................................................................

read_char:
    ; save contents of registers
    push rax
    push rbx
    push rcx
    push rdx

    ; sys_read
    mov rax, sys_read
    mov rbx, stdin
    mov rcx, inp
    mov edx, 1
    int 80h

    ; retrieve contents of registers
    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret

;..............................................................................

evaluate_char:
    ; save contents of registers
    push rax

    ; check quit command
    mov al, byte 'q'
    cmp al, [inp]
    je exit

    ; retrieve contents of registers
    pop rax
    ret

;------------------------------------------------------------------------------

canonical_off:
    call read_stdin_termios

    ; clear canonical bit in local mode flags
    push rax
    mov eax, ICANON
    not eax
    and [termios+12], eax
    pop rax

    call write_stdin_termios
    ret

;..............................................................................

echo_off:
    call read_stdin_termios

    ; clear echo bit in local mode flags
    push rax
    mov eax, ECHO
    not eax
    and [termios+12], eax
    pop rax

    call write_stdin_termios
    ret

;..............................................................................

canonical_on:
    call read_stdin_termios

    ; set canonical bit in local mode flags
    or dword [termios+12], ICANON

    call write_stdin_termios
    ret

;..............................................................................

echo_on:
    call read_stdin_termios

    ; set echo bit in local mode flags
    or dword [termios+12], ECHO

    call write_stdin_termios
    ret

;..............................................................................

read_stdin_termios:
    push rax
    push rbx
    push rcx
    push rdx

    mov eax, 36h
    mov ebx, stdin
    mov ecx, 5401h
    mov edx, termios
    int 80h

    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret

;..............................................................................

write_stdin_termios:
    push rax
    push rbx
    push rcx
    push rdx

    mov eax, 36h
    mov ebx, stdin
    mov ecx, 5402h
    mov edx, termios
    int 80h

    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret
