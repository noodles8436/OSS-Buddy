package com.djy.budy;

import static android.speech.tts.TextToSpeech.ERROR;

import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class ReservationActivity extends AppCompatActivity {
    private TextToSpeech tts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_reservation);
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });
        Button ybutton = (Button) findViewById(R.id.yesbutton);
        Button nbutton = (Button) findViewById(R.id.nobutton);

        ybutton.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                Intent intent = new Intent(ReservationActivity.this, check_res.class);
                Network.reserveBus(com.djy.budy.LoginActivity.identify);//버스 노선번호 가져오기
                startActivity(intent);
            }

            @Override
            public void onSingleClick() {
                tts.speak(com.djy.budy.LoginActivity.identify + "이 맞으십니까? 맞다면 왼쪽 화면을 더블클릭해주세요", TextToSpeech.QUEUE_FLUSH,null);
            }
        });

        nbutton.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                //Intent intent = new Intent(this,//버스 예약버튼 띄우는 레이아웃.class);
                Intent intent = new Intent(ReservationActivity.this, LoginActivity.class);
                startActivity(intent);
            }

            @Override
            public void onSingleClick() {
                tts.speak(com.djy.budy.LoginActivity.identify+"이 아니십니까? 예약하고자 하는 버스가 아니라면 오르쪽 화면을 더블클릭해주세요", TextToSpeech.QUEUE_FLUSH,null);
            }
        });
    }
}