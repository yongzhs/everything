# the functions in the script generates the commands based on Semitech Itron RF PHY API version 5, it does not interact with serial port at all. 
Interface_Common = [0]
# Interface_Itron_IEEE_MAC = 0x82;
# Interface_Itron_IEEE_PHY = 0x88;
#        public const Byte Interface_Itron_RF_MAC = 0xA2;
Interface_Itron_RF_PHY = [0xA8]
#        public const Byte Interface_ControlApp = 0xE0;
#        public const Byte Interface_General_Control = 0xF0;
#        public const Byte Interface_Debug = 0xFB;
#        public const Byte Interface_Text = 0xFE;
#        public const Byte Interface_Network = 0xFF;

REQ_INTERFACE_SUPPORTED = [0, 0]  # Request Interface support status
#        public const int REQ_INTERFACE_ACTIVE = 0x0001;     # Request Interface active status
#        public const int ACTIVATE_INTERFACE = 0x0002;       # Activate Interface
#        public const int DEACTIVATE_INTERFACE = 0x0003;     # De-activate interface
#        public const int INTERFACE_CMD_RESPONSE = 0x0006;   # Interface command response
#        public const int Get_PROTOCOL = 0x000A;             # Get protocol
#        public const int Get_PROTOCOL_Response = 0x000B;    # Get protocol
#        public const int Get_FW_ID = 0x000C;                # Get FW ID
#        public const int Get_FW_ID_Response = 0x000D;       # Get FW ID response
#        public const int INTERFACE_ERROR = 0x00FF;          # Error detected

ITRON_DATA_REQUEST = [1, 0]  # Data Request
ITRON_STATUS_REQUEST = [1, 2]  # Status Request
#        public const int ITRON_PACKET_DURATION    = 0x0103; # Packet Duration

ITRON_CALIBRATION = [1, 4]  # Full Calibration Read
ITRON_RX_START = [1, 5]  # Rx Start
ITRON_TESTMODE_RX_START = [1, 6]  # Test mode Rx Start
#        public const int ITRON_RX_STOP            = 0x0107; // Stop rx
ITRON_TX_STOP = [1, 8]  # Stop tx
#        public const int ITRON_PHY_RESET          = 0x0109; // PHY reset
#        public const int ITRON_PHY_START          = 0x010A; // PHY start
#        public const int ITRON_CCA_ED_REQUEST     = 0x010B; // CCA ED request

ITRON_XCVR_READ_REG = [1, 16]  # Transceiver Read request
ITRON_XCVR_WRITE_REG = [1, 17]  # Transceiver Write request
#        public const int ITRON_DFE_READ_REG       = 0x0112; // DFE Read request
#        public const int ITRON_DFE_WRITE_REG      = 0x0113; // DFE Write request
#        public const int ITRON_XCVR_SET_MODE      = 0x0114; // Transceiver Set Mode request
#        public const int ITRON_XCVR_SET_VCO       = 0x0115; // Transceiver Set VCO request
ITRON_PIBGET_REQUEST = [1, 22]  # PIB get request
ITRON_PIBSET_REQUEST = [1, 23]  # PIB set request
#        public const int ITRON_SET_FEM            = 0x0118; // Configure front-end module
#        public const int ITRON_RFIC_RESET         = 0x0119; // Reset RFIC
#        public const int ITRON_DFE_READ_REG_M     = 0x011A; // DFE Read request for multiple regs
#        public const int ITRON_XCVR_READ_REG_M    = 0x011B; // Transceiver Read request for multiple regs
ITRON_TESTMODE_TX_START = [1, 32]  # Test mode tx
#        public const int ITRON_DIAGNOSTICS_REQUEST= 0x0121; // Diagnostics request
ITRON_OTP_READ = [1, 34]  # OTP read
#        public const int ITRON_OTP_WRITE          = 0x0123; // OTP write
#        public const int ITRON_OTP_CRCREAD        = 0x0124; // OTP read
#        public const int ITRON_OTP_CRCWRITE       = 0x0125; // OTP write
#        public const int ITRON_DATA_CONFIRM       = 0x1100; // Data Confirm
ITRON_DATA_INDICATION = [17, 1]  # Data Indication
ITRON_STATUS_RESPONSE = [17, 2]  # Status Request Response
ITRON_CALIBRATION_RESP = [17, 4] # Calibration
#        public const int ITRON_TESTMODE_RX_CONFIRM= 0x1106; // Test mode Rx Start confirm
#        public const int ITRON_CCA_INDICATION     = 0x1107; // CCA indication
ITRON_PREAMBLE_INDICATION = [17, 8]  # Preamble indication
#        public const int ITRON_PHY_START_RESP     = 0x110A; // PHY start callback
ITRON_RX_START_RESP = [17, 11]  # Rx Start response


#        public const int ITRON_RX_TESTMODE_START_RESP = 0x110C; // Rx Test-mode Start response
#        public const int ITRON_TX_TESTMODE_START_RESP = 0x110D; // Tx Test-mode Start response
#        public const int ITRON_XCVR_READ_REG_RESP = 0x1110; // Transceiver Read request
#        public const int ITRON_XCVR_WRITE_REG_RESP= 0x1111; // Transceiver Write request
#        public const int ITRON_DFE_READ_REG_RESP  = 0x1112; // DFE Read request
#        public const int ITRON_DFE_WRITE_REG_RESP = 0x1113; // DFE Write request
#        public const int ITRON_XCVR_SET_MODE_RESP = 0x1114; // Transceiver Set Mode request response
#        public const int ITRON_XCVR_SET_VCO_RESP  = 0x1115; // Transceiver Set Mode request response
#        public const int ITRON_PIBGET_CONFIRM     = 0x1116; // PIB get confirm
#        public const int ITRON_PIBSET_CONFIRM     = 0x1117; // PIB set confirm
#        public const int ITRON_SET_FEM_RESP       = 0x1118; // Set FEM response
#        public const int ITRON_RFIC_RESET_RESP    = 0x0119; // Reset RFIC response
#        public const int ITRON_DFE_READ_REG_M_RESP= 0x111A; // DFE Read request for multiple regs response
#        public const int ITRON_XCVR_READ_REG_M_RESP=0x111B; // Transceiver Read request for multiple regs response
#        public const int ITRON_RX_STOP_RESP       = 0x111C; // Stop rx response
#        public const int ITRON_TX_STOP_RESP       = 0x111D; // Stop tx response
#        public const int ITRON_CCA_REQUEST_RESPONSE=0x111E; // CCA_ED request response
#        public const int ITRON_TESTMODE_TX_CONFIRM= 0x1120; // Test mode end
#        public const int ITRON_DIAGNOSTICS_RESP   = 0x1121; // Diagnostics response
ITRON_OTP_READ_RESP = [17, 34]  # OTP read response
#        public const int ITRON_OTP_WRITE_RESP     = 0x1123; // OTP write response
#        public const int ITRON_OTP_CRCREAD_RESP   = 0x1124; // OTP read response
#        public const int ITRON_OTP_CRCWRITE_RESP  = 0x1125; // OTP write response

def tx(mod, psdulen, freq, power):
    data = [0 for i in range(40 + psdulen)]
    data[0] = mod
    data[12:14] = UShortTo2Bytes(psdulen)
    data[24:28] = ULongTo4Bytes(freq)
    data[28] = power
    for i in range(psdulen):
        data[40 + i] = i
    return protocol_pack(ITRON_DATA_REQUEST, data)


def tx_stop():  # stop transmitting
    return protocol_pack(ITRON_TX_STOP, [])


def tx_test(mod, psdulen, freq, power, tx_attn_manual, tx_attn_rfic, tx_attn_digital, txContinuousMode, num_packets,
            pkt_intval, txCWMode, antenna_select):
    data = [0 for i in range(72)]
    data[0] = mod
    data[12:14] = UShortTo2Bytes(psdulen)
    data[24:28] = ULongTo4Bytes(freq)
    data[28] = power
    data[40] = tx_attn_manual
    data[41] = tx_attn_rfic
    data[42:44] = UShortTo2Bytes(tx_attn_digital)
    data[44] = txContinuousMode
    data[48] = num_packets
    data[56:60] = ULongTo4Bytes(pkt_intval)
    data[60] = txCWMode
    data[69] = 0x55
    data[70] = antenna_select
    return protocol_pack(ITRON_TESTMODE_TX_START, data)


def rx_config(freq):  # FSK150k OFDM option 1 and 3 and OQPSK
    # data = [0 for i in range(24)]
    # data[0] = 4
    # data[4:7] = [8, 6, 1]
    # data[8:12] = ULongTo4Bytes(freq)
    # data[12] = 8
    #  data[16] = 7
    data = [0 for i in range(28)]
    data[0] = 4
    data[4:7] = [8, 5, 1]
    data[12:16] = ULongTo4Bytes(freq)
    data[16] = 8
    data[20] = 7
    return protocol_pack(ITRON_RX_START, data)


def rx_config_gen(freq):  # SSN FSK and OFDM option 1 and 3
    data = [0 for i in range(28)]
    data[0] = 4
    data[5:7] = [5, 240]
    data[12:16] = ULongTo4Bytes(freq)
    data[18] = 16
    data[20] = 7
    return protocol_pack(ITRON_RX_START, data)


def rx_config_test_mode_gen(freq):
    data = [0 for i in range(52)]
    data[0] = 4
    data[5:7] = [5, 240]  # now supports SSN modulations
    data[12:16] = ULongTo4Bytes(freq)
    data[42] = 0x55
    return protocol_pack(ITRON_TESTMODE_RX_START, data)


def rx_config_test_mode(freq):
    data = [0 for i in range(52)]
    data[0] = 4
    data[4:7] = [8, 5, 1]
    data[12:16] = ULongTo4Bytes(freq)
    data[42] = 0x55
    return protocol_pack(ITRON_TESTMODE_RX_START, data)


def rx_test_mode_get_counters():
    data = [0, 0, 0, 5, 184, 0, 0, 0]
    return protocol_pack(ITRON_PIBGET_REQUEST, data)


def rx_test_mode_clear_counters():
    data = [0] * 192
    data[3] = 0x05
    data[4] = 0xB8
    return protocol_pack(ITRON_PIBSET_REQUEST, data)


def rssi_req():  # noise floor RSSI request
    data = [0, 0, 1, 0, 6, 0]
    return protocol_pack(ITRON_STATUS_REQUEST, data)


def full_cal(): # do full calibration
    data = [12, 0, 0, 0, 0, 197, 13, 0, 0, 0, 0, 0]
    return protocol_pack(ITRON_CALIBRATION, data)
    
 
def full_cal_read():  # full calibration results read only request
    data = [12, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    return protocol_pack(ITRON_CALIBRATION, data)


def reg_read(addr):  # read RFIC register
    data = [int(addr), 0, 0, 0, 0, 0, 0, 0]
    return protocol_pack(ITRON_XCVR_READ_REG, data)


def protocol_pack(cmd, data):  # add delim, check sum and handle exception
    interface = Interface_Itron_RF_PHY
    data_len = [0, len(data)]
    packet = interface + cmd + data_len + data
    checksum = [-sum(packet) % 256]  # checksum and length first, then handle escape
    return tx_escape_handle([60] + packet + checksum + [62])


def protocal_unpack(data):
    t = rx_escape_handle(data)
    data_len = len(t)
    if t[0] == 60 and t[1] == Interface_Itron_RF_PHY[0] and t[data_len - 1] == 62 and (
            t[4] * 256 + t[5]) == data_len - 8 and (sum(t) - 122) % 256 == 0:
        del t[data_len - 2: data_len], t[4:6], t[0:2]  # delete interface checksum etc and leave only cmd and packet
    else:
        return -1
    return t


def tx_escape_handle(t):  # add escape
    for i in range(2, len(t) - 1):  # no need to check delim and interface
        if t[i] == 60 or t[i] == 61 or t[i] == 62:
            t = t[0:i] + [61, 255 - t[i]] + t[i + 1:len(t)]
    # print(t)
    return t


def rx_escape_handle(t):  # remove escape in UART RX
    escape = []
    for i in range(2, len(t) - 1):
        if t[i] == 61:
            escape.append(i)
    for i in range(len(escape)):
        index = escape[i] - i
        t = t[0: index] + [255 - t[index + 1]] + t[index + 2: len(t)]
    return t


def UShortTo2Bytes(s):
    pkt = [0, 0]
    pkt[0] = s & 0xFF
    pkt[1] = (s >> 8) & 0xFF
    return pkt


def ULongTo4Bytes(s):
    pkt = [0, 0, 0, 0]
    pkt[0] = s & 0xFF;
    pkt[1] = (s >> 8) & 0xFF;
    pkt[2] = (s >> 16) & 0xFF;
    pkt[3] = (s >> 24) & 0xFF
    return pkt


def TwoBytesToShort(s):  # input list of 2 elements, convert to signed short integer7fff
    t = s[0] + (s[1] << 8)
    if t <= 32767:
        return t
    else:
        return t - 65536  # struct.unpack("h", s[0:2])


def TwoBytesToUShort(t):
    return (t[1] << 8) + t[0]

# def FourBytesToUShort(t):
#    return (t[3] << 24) + (t[2] << 16) + (t[1] << 8) + t[0]
