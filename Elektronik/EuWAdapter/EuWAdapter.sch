EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_02X05 J5
U 1 1 58F4ACF1
P 3900 1800
F 0 "J5" H 3900 2100 50  0000 C CNN
F 1 "CONN_02X05" H 3900 1500 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Angled_2x05_Pitch2.54mm" H 3900 600 50  0001 C CNN
F 3 "" H 3900 600 50  0001 C CNN
	1    3900 1800
	1    0    0    -1  
$EndComp
Text GLabel 4150 1800 2    60   Input ~ 0
GND
Text GLabel 4150 1900 2    60   Input ~ 0
GND
Text GLabel 4150 2000 2    60   Input ~ 0
GND
$Comp
L CONN_01X03 J2
U 1 1 58F4C205
P 1650 1700
F 0 "J2" H 1650 1900 50  0000 C CNN
F 1 "CONN_01X03" V 1750 1700 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm" H 1650 1700 50  0001 C CNN
F 3 "" H 1650 1700 50  0001 C CNN
	1    1650 1700
	-1   0    0    1   
$EndComp
$Comp
L CONN_01X03 J3
U 1 1 58F4C2D4
P 1650 2150
F 0 "J3" H 1650 2350 50  0000 C CNN
F 1 "CONN_01X03" V 1750 2150 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm" H 1650 2150 50  0001 C CNN
F 3 "" H 1650 2150 50  0001 C CNN
	1    1650 2150
	-1   0    0    1   
$EndComp
$Comp
L CONN_01X02 J4
U 1 1 58F4C3BE
P 1650 2600
F 0 "J4" H 1650 2750 50  0000 C CNN
F 1 "CONN_01X02" V 1750 2600 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 1650 2600 50  0001 C CNN
F 3 "" H 1650 2600 50  0001 C CNN
	1    1650 2600
	-1   0    0    1   
$EndComp
$Comp
L CONN_01X02 J1
U 1 1 58F4C3F9
P 1600 3100
F 0 "J1" H 1600 3250 50  0000 C CNN
F 1 "CONN_01X02" V 1700 3100 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 1600 3100 50  0001 C CNN
F 3 "" H 1600 3100 50  0001 C CNN
	1    1600 3100
	-1   0    0    1   
$EndComp
$Comp
L TIP120 Q1
U 1 1 58F4C490
P 3900 2750
F 0 "Q1" H 4150 2825 50  0000 L CNN
F 1 "TIP120" H 4150 2750 50  0000 L CNN
F 2 "TO_SOT_Packages_THT:TO-220_Vertical" H 4150 2675 50  0001 L CIN
F 3 "" H 3900 2750 50  0001 L CNN
	1    3900 2750
	0    -1   -1   0   
$EndComp
$Comp
L R R2
U 1 1 58F4CA39
P 3500 1900
F 0 "R2" V 3580 1900 50  0000 C CNN
F 1 "R" V 3500 1900 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 3430 1900 50  0001 C CNN
F 3 "" H 3500 1900 50  0001 C CNN
	1    3500 1900
	0    1    1    0   
$EndComp
Wire Wire Line
	4150 1800 4150 2650
Connection ~ 4150 1900
Wire Wire Line
	4150 1350 4150 1700
Wire Wire Line
	3350 2950 3900 2950
Wire Wire Line
	4150 2650 4100 2650
Connection ~ 4150 2000
Wire Wire Line
	1850 1800 2150 1800
Wire Wire Line
	2150 1800 2150 2250
Wire Wire Line
	2150 2250 1850 2250
Wire Wire Line
	2150 2000 2900 2000
Wire Wire Line
	2900 2650 3700 2650
Connection ~ 2150 2000
Wire Wire Line
	1850 2150 2350 2150
Wire Wire Line
	2350 1700 2350 3050
Wire Wire Line
	1850 1700 2900 1700
Wire Wire Line
	2900 1700 2900 1350
Wire Wire Line
	2900 1350 4150 1350
Connection ~ 4150 1600
Connection ~ 2350 1700
Wire Wire Line
	1850 2050 2650 2050
Wire Wire Line
	2650 2050 2650 1750
Wire Wire Line
	2650 1750 3400 1750
Wire Wire Line
	3400 1750 3400 1700
Wire Wire Line
	2800 2550 1850 2550
Wire Wire Line
	2800 1800 2800 2550
Wire Wire Line
	1850 2650 2750 2650
Wire Wire Line
	2750 2650 2750 2100
Wire Wire Line
	2750 2100 3100 2100
Wire Wire Line
	3100 2100 3100 1500
Wire Wire Line
	2900 2000 2900 2250
Wire Wire Line
	2900 2250 4150 2250
Connection ~ 4150 2250
Wire Wire Line
	2900 2650 2900 3150
Wire Wire Line
	2900 3150 1800 3150
Wire Wire Line
	2350 3050 1800 3050
Connection ~ 2350 2150
$Comp
L R R1
U 1 1 58F4D74D
P 2950 2400
F 0 "R1" V 3030 2400 50  0000 C CNN
F 1 "R" V 2950 2400 50  0000 C CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 2880 2400 50  0001 C CNN
F 3 "" H 2950 2400 50  0001 C CNN
	1    2950 2400
	0    1    1    0   
$EndComp
Wire Wire Line
	3100 2400 3100 2250
Connection ~ 3100 2250
Connection ~ 2850 2400
Connection ~ 2800 2400
Wire Wire Line
	3400 1700 3550 1700
Wire Wire Line
	3100 1500 3400 1500
Wire Wire Line
	3400 1500 3450 1650
Wire Wire Line
	3450 1650 3600 1650
Wire Wire Line
	3600 1650 3650 1700
Wire Wire Line
	2800 1800 3200 1800
Wire Wire Line
	3200 1800 3200 1600
Wire Wire Line
	3200 1600 3650 1600
Wire Wire Line
	3550 1700 3650 1800
Wire Wire Line
	3350 1900 3350 2950
Wire Wire Line
	3650 2000 1850 1600
$EndSCHEMATC
