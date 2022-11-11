package com.djy.budy;

import static android.speech.tts.TextToSpeech.ERROR;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.speech.tts.TextToSpeech;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class Get_Off extends AppCompatActivity {
    private TextToSpeech tts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_get_off);
        Button Send_Alert = (Button)findViewById(R.id.send_alert);

        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != ERROR) {
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });

        Send_Alert.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                Handler handler = new Handler();
                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        new Thread(){
                            public void run(){
                                Network.done();
                            }
                        }.start();
                        Intent intent = new Intent(Get_Off.this, MainActivity.class); //화면 전환
                        startActivity(intent);
                        tts.speak("하차 알림이 전송되었습니다. 이용해주셔서 감사합니다.", TextToSpeech.QUEUE_FLUSH,null);
                        finish();
                    }
                }, 1000);
            }

            @Override
            public void onSingleClick() {
                tts.speak("하차 알림을 전송하시려면 화면을 더블클릭해주세요.", TextToSpeech.QUEUE_FLUSH,null);
            }
        });
    }


}