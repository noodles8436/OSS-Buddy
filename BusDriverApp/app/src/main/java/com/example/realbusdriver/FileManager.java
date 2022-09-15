package com.example.realbusdriver;


import android.content.Context;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

public class FileManager {

    private static final String FILE_NAME = "userdata.config";

    Context mContext;

    public FileManager(Context context) {
        mContext = context;
    }

    private void save(String strData) {
        if( strData == null || strData.equals("") ) {
            return;
        }

        FileOutputStream fosMemo = null;

        try {
            // 파일에 데이터를 쓰기 위해서 output 스트림 생성
            fosMemo = mContext.openFileOutput(FILE_NAME, Context.MODE_PRIVATE);
            // 파일에 메모 적기
            fosMemo.write( strData.getBytes() );
            fosMemo.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 저장된 메모를 불러오는 함수
    private String load() {
        try {
            // 파일에서 데이터를 읽기 위해서 input 스트림 생성
            FileInputStream fisMemo = mContext.openFileInput(FILE_NAME);

            // 데이터를 읽어 온 뒤, String 타입 객체로 반환
            byte[] memoData = new byte[fisMemo.available()];
            while (fisMemo.read(memoData) != -1) { }

            return new String(memoData);
        } catch (IOException e) {  }

        return null;
    }

    // 저장된 메모를 삭제하는 함수
    private void delete() {
        mContext.deleteFile(FILE_NAME);
    }

    public void saveBusDriver(String _name, String _UID, String vehicleNo, String routeNo) {
        delete();
        String result = _name + ":" + _UID + ":" + vehicleNo + ":" + routeNo;
        save(result);
    }

    // BUS DRIVER METHOD

    public String getDriverName() {
        if(isDriverExist()) {
            String[] result = load().split(":");
            return result[0];
        }else {
            return null;
        }
    }

    public String getDriverUID() {
        if(isDriverExist()) {
            String[] result = load().split(":");
            return result[1];
        }else {
            return null;
        }
    }

    public String getDriverVehicleNo() {
        if(isDriverExist()) {
            String[] result = load().split(":");
            return result[2];
        }else {
            return null;
        }
    }

    public String getDriverRouteNo() {
        if(isDriverExist()) {
            String[] result = load().split(":");
            return result[3];
        }else {
            return null;
        }
    }

    public boolean isDriverExist() {
        String result = load();
        if(result == null) {
            return false;
        }
        return true;
    }



}
