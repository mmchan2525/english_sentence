import asyncio
import os
import subprocess
import sys

# 99 Phrases list
PHRASES = [
    (1, "I wipe off the sweat.", "汗を拭く"),
    (2, "You are so sweaty!", "すっごい汗かいてるよ！"),
    (3, "I sweat easily.", "私汗っかきなの"),
    (4, "I broke into a cold sweat.", "冷や汗かいた"),
    (5, "I missed my flight!", "飛行機に乗り遅れた"),
    (6, "I got on the train heading in the opposite direction.", "反対方向行きの電車に乗ってしまった"),
    (7, "I missed my stop!", "乗り過ごした！"),
    (8, "I got on the wrong bus by mistake.", "間違って違うバスに乗ってしまった"),
    (9, "I got off at the wrong station.", "降りる駅間違えた"),
    (10, "I couldn’t pass through the ticket gate because I didn’t have enough money on my card.", "カードの残高不足で自動改札が通れなかった"),
    (11, "Your shirt is inside out!", "シャツ表裏反対になってるよ！"),
    (12, "I put my shirt on backwards!", "シャツを前後ろ反対に着てしまった"),
    (13, "I had buttoned up my shirt wrong.", "シャツのボタンを掛け違えた！"),
    (14, "The button on your shirt has come off.", "シャツのボタン取れてるよ！"),
    (15, "Your zipper is open.", "ファスナー開いてるよ"),
    (16, "I’ll do up the button for you.", "ボタン留めてあげるよ"),
    (17, "The thread is coming loose.", "糸がほつれているよ"),
    (18, "My shirt is all wrinkled.", "シャツしわくちゃだ！"),
    (19, "There is a hole in my sock!", "靴下に穴が空いている！"),
    (20, "The seat of my pants is shiny.", "ズボンのお尻部分がテカテカしている"),
    (21, "Sorry, I was spacing out.", "ごめん、ぼーっとしてた。"),
    (22, "It slipped my mind.", "ど忘れした！"),
    (23, "I was a little irritated.", "ちょっとイラっときた"),
    (24, "It tugged at my heartstrings.", "うるっときた"),
    (25, "It’s really heartwarming.", "ほっこりするね"),
    (26, "I’m feeling antsy.", "そわそわする"),
    (27, "No worries!", "気にしてないよ"),
    (28, "I can’t concentrate!", "集中できない"),
    (29, "Feels nice!", "気持ちいい〜"),
    (30, "That’s annoying!", "ウザッ！"),
    (31, "You have smooth skin!", "肌ツルツルだよね！"),
    (32, "My skin is dry and rough.", "肌カサカサだ！"),
    (33, "Her hair is smooth and silky.", "彼女の髪サラサラね。"),
    (34, "You have big beady eyes.", "目ぱっちりしてるね"),
    (35, "He has almond eyes.", "彼の目、切れ長だね。"),
    (36, "You have a shapely nose.", "鼻筋通ってるね"),
    (37, "His baby tooth fell out yesterday.", "昨日彼の乳歯が抜けた。"),
    (38, "If you don’t brush your teeth, you will get a cavity.", "歯磨きしないと虫歯になるよ！"),
    (39, "Beautiful nails. Where did you get them done?", "きれいなネイルね。どこでやってもらったの？"),
    (40, "Your hairstyle really suits you. Where did you get your hair cut?", "その髪型似合ってるね。どこで切ってもらったの？"),
    (41, "This picture is blurry.", "この写真ぼやけてるね。"),
    (42, "People in the front, please crouch down!", "前列の人はしゃがんでください"),
    (43, "Move to the right a bit.", "少し右に寄ってください。"),
    (44, "Please squeeze in.", "ぎゅっと詰めてください。"),
    (45, "What do you want in the background?", "背景に何を入れましょうか？"),
    (46, "Would you like to check the photos?", "写真を確認してもらえますか？"),
    (47, "Could you please take a photo of us?", "写真を撮ってもらえますか？"),
    (48, "Would you like me to take your photo?", "写真撮りましょうか？"),
    (49, "Could you take it in landscape mode?", "横向きで撮ってもらえますか？"),
    (50, "Could you take it vertically?", "縦向きで撮ってもらえますか？"),
    (51, "That name rings a bell.", "その名前聞き覚えがある。"),
    (52, "I can’t put a face to the name.", "名前と顔が一致しない"),
    (53, "That face rings a bell.", "その顔見覚えがある。"),
    (54, "I can’t put a name to the face.", "顔と名前が一致しない"),
    (55, "Does it ring a bell?", "心当たりある？ピンとくる？"),
    (56, "It’s on the tip of my tongue.", "喉まで出かかってるんだけど。"),
    (57, "It looks like a familiar scenery.", "見覚えのある景色だ。"),
    (58, "What a coincidence!!", "すっごい偶然！"),
    (59, "It never occurred to me.", "思っても見なかった。"),
    (60, "It’s surprising!", "意外！"),
    (61, "My hands are sticky.", "手がベタベタする。"),
    (62, "It’s too spicy for me. My mouth is burning.", "私には辛すぎる！口がヒリヒリする！"),
    (63, "It’s crispy on the outside, fluffy on the inside!", "外はサクサク、中はふわふわ！"),
    (64, "It melts in my mouth!", "口の中でとろけるよ！"),
    (65, "This no-bake cheesecake is rich and thick.", "このレアチーズケーキ濃厚だね。"),
    (66, "Natto is very smelly and sticky.", "納豆はとても臭くてネバネバしています。"),
    (67, "I like squid because it’s chewy.", "イカは歯ごたえがあるので好きです。"),
    (68, "This omelette is soft and moist.", "このオムレツとろっとろだね。"),
    (69, "Wasabi stings my nose.", "わさびは鼻にツーンとくる。"),
    (70, "I like this texture.", "この食感が好き"),
    (71, "We’re not on the same page.", "私たち話噛み合ってないよね。"),
    (72, "She never speaks ill of others.", "彼女は決して他の人の悪口を言わない。"),
    (73, "He always exaggerates things.", "彼はいつも言うことが大袈裟だ。"),
    (74, "He always makes sarcastic comments.", "彼はいつも嫌味を言う。"),
    (75, "She is a good listener.", "彼女は聞き上手だ。"),
    (76, "You are the only one I can talk to.", "話せるのはあなただけです。"),
    (77, "She always interrupts a conversation.", "彼女はいつも人の話に割り込んでくる。"),
    (78, "I can't get used to his harsh words.", "彼のトゲのある言い方に慣れることができない。"),
    (79, "He blamed me in a roundabout way.", "彼は遠回しに私を非難した。"),
    (80, "His stories are interesting.", "彼は話が面白い"),
    (81, "I have a hangover.", "二日酔いだ。"),
    (82, "I got food poisoning.", "食べ物にあたった。"),
    (83, "I have a leg cramp.", "足がつった！"),
    (84, "I’m sore from playing badminton yesterday.", "昨日のバドミントンで筋肉痛になった。"),
    (85, "I’m allergic to nuts.", "私はナッツアレルギーです。"),
    (86, "I have a pollen allergy.", "私は花粉症です。"),
    (87, "I’m on my period.", "生理中なの"),
    (88, "I don’t feel like doing anything today.", "今日は何もする気にならない。"),
    (89, "I don’t want to get sunburned.", "日焼けしたくない"),
    (90, "I almost got heat stroke.", "熱中症になりかけた。"),
    (91, "It’s a lovely day!", "いい天気だね！"),
    (92, "The breeze feels great.", "風が気持ちいい。"),
    (93, "Let’s go into the shade.", "日陰に入ろう。"),
    (94, "I can’t see ahead because of the heavy rain.", "雨が激しくて前が見えない。"),
    (95, "I hear thunder.", "雷が鳴ってる。"),
    (96, "The lightning struck nearby last night.", "昨日の夜近くに雷が落ちた"),
    (97, "Make sure to stay hydrated.", "忘れずに水分補給してね"),
    (98, "I’ll let you go.", "話はこのくらいで。そろそろ失礼します。"),
    (99, "Stay safe and cool!", "涼しくして体調に気をつけてね。")
]

async def generate_with_edge_tts():
    try:
        import edge_tts
    except ImportError:
        print("edge-tts が見つかりません。インストールを試みます...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
        import edge_tts

    out_dir = os.path.join(os.path.dirname(__file__), "audio_files")
    os.makedirs(out_dir, exist_ok=True)
    print(f"音声ファイルの保存先: {out_dir}")

    voice_en = "en-US-JennyNeural"  # 高品質な英語女性音声
    voice_ja = "ja-JP-NanamiNeural" # 高品質な日本語女性音声

    print(f"全 {len(PHRASES)} 件の音声を生成中...")

    for num, en, ja in PHRASES:
        filename = f"{num:02d}.mp3"
        filepath = os.path.join(out_dir, filename)
        
        # 英語音声
        communicate_en = edge_tts.Communicate(f"Number {num}. {en}", voice_en)
        await communicate_en.save(filepath)
        print(f"[{num}/{len(PHRASES)}] 生成完了: {filename} ({en})")

    print("\nすべての個別MP3音声の生成が完了しました！")

if __name__ == "__main__":
    asyncio.run(generate_with_edge_tts())
