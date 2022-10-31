/*
OSS-BUDDY : Smart Bus Boarding System for the Blind
Copyright (C) 2022 OSS-BUDDY Authors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
*/

package com.example.realbusdriver;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

public class BD_loginActivity extends AppCompatActivity {

    private Thread getReserveThread = null;
    private boolean isRunThread = false;
    private BusReserve busReserve = null;

    public static TextView busstop = null;
    public static TextView prebus = null;
    public static TextView busdrivername = null;
    public static TextView busroutenum= null;

    @SuppressLint({"SetTextI18n", "HandlerLeak"})
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bdlogin);

        busstop=(TextView) findViewById(R.id.busstopname);
        prebus=(TextView) findViewById(R.id.prebus);
        busdrivername=(TextView) findViewById(R.id.busdrivername);
        busroutenum=(TextView) findViewById(R.id.busnumber);

        //서버에서 에약현황 넘겨주기
        final Handler handler = new Handler(){
            public void handleMessage(Message msg){
                BusReserve bus = NetworkBus.getReserveStation();
                if(bus == null){
                    prebus.setText("");
                    busstop.setText("예약한 사람이 없습니다");
                }else{
                    prebus.setText(bus.getArrivalLeftNode() + "정거장 뒤");
                    busstop.setText("정거장 이름: "+ bus.getStationName()+" 에 "+"\n"+"예약한 사람이 있습니다.");
                }
            }
        };

        busroutenum.setText(NetworkBus.getDriverRouteNo()+"번 버스 운행");
        busdrivername.setText("버스기사이름: "+NetworkBus.getDriverName()+"기사님");

        getReserveThread = new Thread(){
            @Override
            public void run() {
                isRunThread = true;
                while (isRunThread){
                    Message msg = handler.obtainMessage();
                    handler.sendMessage(msg);
                    try {
                        sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        };

        runThread();

    }

    private void runThread(){
        getReserveThread.start();
    }

    private void stopThread(){
        isRunThread = false;
    }
}
