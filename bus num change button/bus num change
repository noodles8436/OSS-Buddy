package com.example.changebusnum;

import static android.speech.tts.TextToSpeech.ERROR;

import android.os.Handler;
import android.os.SystemClock;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.GestureDetector;
import android.view.View;
import android.widget.Button;

import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private TextToSpeech tts;
    int busn=0;
    int[] busnum = {22,23,24};
    final int[] identify = {0};
    final int[] k = {0};
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });

        Button resbutton = (Button) findViewById(R.id.reservation);
        final int[] number_of_clicks = {0};
        final boolean[] thread_started = {false};
        final int DELAY_BETWEEN_CLICKS_IN_MILLISECONDS = 250;

        resbutton.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                k[0] = changnum(busnum);
                identify[0] = k[0];
                resbutton.setText(String.valueOf(k[0]));
                tts.speak(String.valueOf(resbutton.getText()), TextToSpeech.QUEUE_FLUSH,null);


            }

            @Override
            public void onSingleClick() {
                tts.speak(String.valueOf(resbutton.getText()), TextToSpeech.QUEUE_FLUSH,null);

            }
        });
        resbutton.setOnLongClickListener(new View.OnLongClickListener() {
            //길게 클릭할 때
            @Override
            public boolean onLongClick(View view) {
                if (identify[0]==0) {
                    tts.speak("버스를 찾으시려면 더블클릭으로 넘겨주세요", TextToSpeech.QUEUE_FLUSH, null);
                } else {
                    tts.speak(String.valueOf(identify[0]) + "버스로 예약하시겠습니까?", TextToSpeech.QUEUE_FLUSH, null);

                }
                return false;
            }
        });
    }

    public int changnum(int[] bnum) {
        if (busn >= bnum.length - 1) {
            busn = 0;
        } else
            busn++;
        int resultbnum = bnum[busn];

        return resultbnum;
    }
}
