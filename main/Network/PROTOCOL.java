package oss;

public class PROTOCOL {
	
	static final String TASK_SPLIT = ";";
	static final int READ_TIME_OUT = 600;
	static final int PACKET_SIZE = 1024;
	
	static final String CONNECTION_CHECK = "CONNECTION_CHECK";
	
	static final String USER_LOGIN = "01";
	static final String USER_LOGIN_SUCCESS = USER_LOGIN + TASK_SPLIT + "00";
	static final String USER_LOGIN_FAIL = USER_LOGIN + TASK_SPLIT + "01";
	static final String USER_LOGIN_SERVER_ERR = USER_LOGIN + TASK_SPLIT + "02";
	static final String USER_LOGIN_CLIENT_ERR = USER_LOGIN + TASK_SPLIT + "03";
	
	
	static final String USER_LOCATION_FIND = "02";
	static final String USER_LOCATION_FIND_SUCCESS = USER_LOCATION_FIND + TASK_SPLIT + "00";
	static final String USER_LOCATION_FIND_FAIL = USER_LOCATION_FIND + TASK_SPLIT + "01";
	
	static final String USER_BUS_CAN_RESERVATION = "03";
	static final String USER_BUS_CAN_RESERVATION_OK = USER_BUS_CAN_RESERVATION + TASK_SPLIT + "00";
	static final String USER_BUS_CAN_RESERVATION_NO = USER_BUS_CAN_RESERVATION + TASK_SPLIT + "01";
			
	static final String USER_BUS_RESERVATION_CONFIRM = "04";
	static final String USER_BUS_RESERVATION_CONFIRM_SUCCESS = USER_BUS_RESERVATION_CONFIRM + TASK_SPLIT + "00";
	static final String USER_BUS_RESERVATION_CONFIRM_FAIL = USER_BUS_RESERVATION_CONFIRM + TASK_SPLIT + "01";
			
	static final String USER_BUS_CANCEL = "05";
	static final String USER_BUS_CANCEL_SUCCESS = USER_BUS_CANCEL + TASK_SPLIT + "00";
	static final String USER_BUS_CANCEL_FAIL = USER_BUS_CANCEL + TASK_SPLIT + "01";
			
	static final String USER_BUS_ARRIVED_VIBE = "06";
			
	static final String KICK_USER = "07" + TASK_SPLIT + "00";
			
	static final String DISCONNECT_SERVER = "08" + TASK_SPLIT + "00";
			
	static final String USER_GPS_LOGIN = "09";

	static final String USER_GPS_LOGIN_SUCCESS = USER_GPS_LOGIN + TASK_SPLIT + "00";
	static final String USER_GPS_LOGIN_FAIL = USER_GPS_LOGIN + TASK_SPLIT + "01";
			
	static final String USER_GPS_DATA = "10";
	
	static final String USER_REQ_BUS_LIST = "11";
}
