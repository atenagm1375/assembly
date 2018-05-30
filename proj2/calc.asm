; Ashena G.Mohammadi
; calculator with the simple arithmetic functions-summation, multiplication,
; division, and subtraction-for both integers and floating point numbers

section .data
    msg db "Enter a valid operation or x to exit:", 10
    msg_len equ $-msg
    errormsg db "Illegal operation. Please, try again.", 10
    error_len equ $-errormsg
    divide_by_zero db "divide by zero", 10
    div_len equ $-divide_by_zero
    result dq 0
    max_num_size equ 19                 ; max digits of a number
    max_op_size equ 38
    max_inp_size equ 200                ; max size of input string

section .bss
    inp resb max_inp_size               ; keeps the input
    num resb max_num_size              ; keeps a number
    op resb max_num_size                           ; keeps operator
    flag resb 1                         ; flags

section .text
    global _start

_start:
    xor bl, bl
    mov byte[flag], bl
    mov rax, 1
    mov rdi, 0
    mov rsi, msg                        ; start message
    mov rdx, msg_len
    syscall

    start_while:
    call readUserInput
    cmp [rsi], byte 'q'
    je exit
    call evaluateInput
    mov bl, 1
    cmp byte[flag], bl
    je _start
    jmp start_while

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

readUserInput:
    mov rcx, max_inp_size
    mov rsi, inp
    xor bl, bl
    clear_while:                        ; clear input buffer before reading a new input
        mov [rsi], bl
        inc rsi
        loop clear_while
    ; sys_read: %rax: 0, %rdi: unsigned int fd, %rsi: char *buf, %rdx: size_t count
    mov rax, 0
    mov rdi, 0
    mov rsi, inp
    mov rdx, max_inp_size
    syscall
    ret

error:
    mov rax, 1
    mov rdi, 0
    mov rsi, errormsg
    mov rdx, error_len
    syscall
    mov bl, 1
    mov byte[flag], 1
    ; TODO: add clear num and clear op
    ret

evaluateInput:
    mov rsi, inp
    mov rdi, num
    mov rcx, max_inp_size
    mov r14, op
    evaluate_while:
        mov r15b, byte[rsi]
        cmp r15b, byte '0'
        jl NAN
        cmp r15b, byte '9'
        jg NAN
        ; TODO: convert string to integer
        inc rsi
        jmp evaluate_while

    NAN:
    cmp r15b, byte '='
    je continue_eval

    cmp r15b, byte '+'
    je continue_eval

    cmp r15b, byte '-'
    je continue_eval

    cmp r15b, byte '*'
    je continue_eval

    cmp r15b, byte '/'
    je continue_eval

    cmp r15b, byte '.'
    je continue_eval

    cmp r15b, byte '('
    je continue_eval

    cmp r15b, byte ')'
    je continue_eval
    call error
    ret

    continue_eval:
    cmp r15b, byte '='
    je end_eval
    mov byte[r14], r15b
    inc r14
    inc rsi
    jmp evaluate_while

    end_eval:
    ret
