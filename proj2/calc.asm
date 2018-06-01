; Ashena G.Mohammadi
; calculator with the simple arithmetic functions-summation, multiplication,
; division, and subtraction-for both integers and floating point numbers

section .data
    msg db "Enter a valid operation or q to exit:", 10
    msg_len equ $-msg
    errormsg db "Illegal operation. Please, try again.", 10
    error_len equ $-errormsg
    divide_by_zero db "divide by zero", 10
    div_len equ $-divide_by_zero
    precission db 0
    tmp dq 0
    max_num_size equ 40                 ; max digits of a number
    max_op_size equ 40
    max_inp_size equ 200                ; max size of input string

section .bss
    inp resb max_inp_size               ; keeps the input
    num resq max_num_size              ; keeps a number
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
    mov bx, 1
    btr [flag], bx
    jc _start
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
    mov bx, 1
    bts [flag], bx
    ; TODO: add clear num and clear op
    ret

atoi:
    push rax
    push rbx
    push rcx
    mov r10, 10
    sub r15b, byte '0'
    mov bx, 2
    bt [flag], bx
    jc toFloat
    mov rax, [rdi]
    mul r10
    add rax, r15
    mov [rdi], rax
    jmp end_atoi

    toFloat:
    xor cl, cl
    cmp cl, byte [precission]
    jne isNotInt
    fild qword [rdi]
    jmp continue_float
    isNotInt:
    fld qword [rdi]
    continue_float:
    inc byte [precission]
    movzx r15, r15b
    mov [tmp], r15
    fild qword [tmp]
    mov [tmp], r10
    fild qword [tmp]
    fstp qword [tmp]
    float_while:
        cmp cl, byte [precission]
        je end_float_while
        fdiv qword [tmp]
        z:inc cl
        jmp float_while
    end_float_while:
    faddp st1, st0
    x:fstp qword [rdi]

    end_atoi:
    pop rcx
    pop rbx
    pop rax
    ret

evaluateInput:
    mov rsi, inp
    mov rdi, num
    mov rcx, max_op_size
    mov r14, op
    evaluate_while:
        mov r15b, byte[rsi]
        cmp r15, byte '.'
        je isFloat
        cmp r15b, byte '0'
        jl NAN
        cmp r15b, byte '9'
        jg NAN
        ; TODO: convert string to integer
        mov bx, 3
        bts [flag], bx
        call atoi
        inc rsi
        jmp evaluate_while
        isFloat:
        mov bx, 2
        bts [flag], bx
        inc rsi
        jmp evaluate_while

    NAN:
    mov bx, 2
    btr [flag], bx
    btr [flag], bx
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

    cmp r15b, byte '('
    je continue_eval

    cmp r15b, byte ')'
    je continue_eval
    call error
    ret

    continue_eval:
    dec rcx
    cmp rcx, 0
    jge valid_size
    call error
    ret
    valid_size:
    mov bx, 3
    btr [flag], bx
    jnc no_num
    inc rdi
    xor bl, bl
    mov [precission], bl
    no_num:
    cmp r15b, byte '='
    je end_eval
    mov byte[r14], r15b
    inc r14
    inc rsi
    jmp evaluate_while

    end_eval:
    ret
