package com.djy.budy;

import static android.speech.tts.TextToSpeech.ERROR;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.speech.tts.TextToSpeech;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class Loading_page extends AppCompatActivity {

    private TextToSpeech tts;
    private static Thread gpsThread = null;
    private static boolean isRunThread = false;
    private GPSTracker gps;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading_page);
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            public void run() {
                // Intent intent = new Intent(getBaseContext(), User_select.class);
                // startActivity(intent);
                Network.readyforLocation();
                startActivity(new Intent(Loading_page.this, LoginActivity.class));
                finish();
            }
        }, 3000);
        gps = new GPSTracker(Loading_page.this);
        startGPS();
    }

    private void startGPS(){
        if(gpsThread == null){
            gpsThread = new Thread(){
                public void run(){
                    isRunThread = true;
                    while(isRunThread){
                        gps.getLocation();
                        Network.setUserLati(gps.getLatitude());
                        Network.setUserLong(gps.getLongitude());
                        try {
                            sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            };
        }
        gpsThread.start();
    }

    private void stopGPS(){
        if(gpsThread != null){
            isRunThread = false;
        }
    }

}

