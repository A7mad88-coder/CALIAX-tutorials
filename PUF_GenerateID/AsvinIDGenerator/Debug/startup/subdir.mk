################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../startup/boot_multicore_slave.c \
../startup/startup_lpc55s69_cm33_core0.c 

OBJS += \
./startup/boot_multicore_slave.o \
./startup/startup_lpc55s69_cm33_core0.o 

C_DEPS += \
./startup/boot_multicore_slave.d \
./startup/startup_lpc55s69_cm33_core0.d 


# Each subdirectory must supply rules for building sources it contributes
startup/%.o: ../startup/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -D__REDLIB__ -DCPU_LPC55S69JBD100 -DCPU_LPC55S69JBD100_cm33 -DCPU_LPC55S69JBD100_cm33_core0 -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -DFSL_RTOS_BM -DSDK_OS_BAREMETAL -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\drivers" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\serial_manager" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS_driver" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\device" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\board" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\utilities" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\lists" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\uart" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\board" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\source" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\drivers" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\device" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\CMSIS_driver" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\startup" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\utilities" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\serial_manager" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\lists" -I"C:\Users\omkar\Documents\MCUXpressoIDE_11.2.1_4149\workspace\asvinid-esp-at\AsvinIDGeneator\component\uart" -O0 -fno-common -g3 -Wall -mcpu=cortex-m33  -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmerge-constants -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m33 -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


