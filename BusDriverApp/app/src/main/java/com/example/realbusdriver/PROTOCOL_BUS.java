package com.example.realbusdriver;


public class PROTOCOL_BUS {

    static final String TASK_SPLIT = ";";
    static final int SERVER_PACKET_SIZE = 1024;

    static final String BUSDRIVER_REGISTER = "20";
    static final String BUSDRIVER_REGISTER_SUCCESS = "00";
    static final String BUSDRIVER_REGISTER_FAIL = "01";

    static final String BUSDRIVER_LOGIN = "21";
    static final String BUSDRIVER_LOGIN_SUCCESS = BUSDRIVER_LOGIN + TASK_SPLIT + "00";
    static final String BUSDRIVER_LOGIN_FAIL = BUSDRIVER_LOGIN + TASK_SPLIT + "01";
    static final String BUSDRIVER_LOGIN_ERR = BUSDRIVER_LOGIN + TASK_SPLIT + "02";

    static final String BUSDRIVER_NODE_ANNOUNCE = "22";

}