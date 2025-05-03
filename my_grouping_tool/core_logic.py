
import pandas as pd
import numpy as np
import random
rng = np.random.default_rng()
import itertools
import sys
import os
import io
# ファイルの権限を変更
#os.chmod('C:/Users/youta/OneDrive/ドキュメント/LEC.xlsx', 0o755)
#f = pd.read_excel('C:/Users/youta/Downloads/2024年度後期L.E.C参加申し込みフォーム(2024 2nd semester L.E (version 2).xlsx')


#ある曜日から各空きコマを取り出し、空きコマを1とする。
#numはある曜日の列番号

def process_grouping(df):

    buffer = io.StringIO()
    sys_stdout = sys.stdout  # 元の標準出力を保存

    try:
        sys.stdout = buffer  # 標準出力を buffer に切り替え

        # ↓ここで自由にprintしまくってOK！
        #print("データの先頭5行：")
        #print(df.head())

        print("\n--- グループ分け処理 ---")
        # あなたの複雑な処理いろいろ…
        # 例:
        # grouped_df = custom_grouping(df)
        # print(grouped_df)

        # 処理が終わったら buffer にたまった文字列を取得
        



    
    
    
    
        def free_class(num,tx):
            empty_v=[]
            for row in df.values:
                v = str(row[num])
                if tx in v:
                    empty_v.append(1)
                else:
                    empty_v.append(0)
            return empty_v


    #native_langu_numは母国語の列番号、Eng_or_Jap_numは英語か日本語の選択の列番号（excelでの１列目は0。）
    #日本人を1、留学生を2、英語の話せない留学生を3とする。
        def separate_group(native_langu_num, Eng_or_Jap_num):
            empty_w=[]
            for row in df.values:
                w = str(row[native_langu_num])
                x = str(row[Eng_or_Jap_num])
                if 'Japanese' in w:
                    empty_w.append(1)
                else:
                    if 'English' in x:
                        empty_w.append(2)
                    else:
                        empty_w.append(3)
            return empty_w


    #ペア希望を1、グループ希望を2、どちらでもを3とする。
        def pair_or_group(pair_num):
            empty_p=[]
            for row in df.values:
                p = str(row[pair_num])
                if 'ペア / pair' in p:
                    empty_p.append(1)
                elif 'グループ / group' in p:
                    empty_p.append(2)
                else:
                    empty_p.append(3)
            return empty_p

    #女を1、男を2、その他を3とする。
        def gender(sex_num):
            empty_g=[]
            for row in df.values:
                g = str(row[sex_num])
                if '男 / male' in g:
                    empty_g.append(2)
                elif '女 / female' in g:
                    empty_g.append(1)
                else:
                    empty_g.append(3)
            return empty_g


    #中国人を1、その他を2とする。
    #def country(country_num):
        #empty_c=[]
        #for row in df.values:
            #c = str(row[country_num])
            #if 'Chinese' in c:
                #empty_c.append(1)
            #else:
                #empty_c.append(2)
        #return empty_c


    #ある曜日の2限から5限の予定をまとめて出力
        def free_class_matrix(day):
        #データの個数を取得
            count_data = df.shape[0]
            pre_mat = np.zeros((5,count_data))
        #関数free_class(num,tx)を使用。
            for x in range(0,count_data):
                pre_mat[0][x] = free_class(day,'2限 (2nd period)')[x]
            for x in range(0,count_data):
                pre_mat[1][x] = free_class(day,'昼休み (Lunch Break)')[x]
            for x in range(0,count_data):
                pre_mat[2][x] = free_class(day,'3限 (3rd period)')[x]
            for x in range(0,count_data):
                pre_mat[3][x] = free_class(day,'4限 (4th period)')[x]
            for x in range(0,count_data):
                pre_mat[4][x] = free_class(day,'5限 (5th period)')[x]
        #見やすいように転置
            pre_mat_T = pre_mat.T
            return pre_mat_T


    #関数free_class_matrix(day)を使用。
        mon = free_class_matrix(15)
        tue = free_class_matrix(16)
        wed = free_class_matrix(17)
        thu = free_class_matrix(18)
        fri = free_class_matrix(19)


    #月曜から金曜までの全ての予定をまとめる
        schedule = np.concatenate([mon,tue,wed,thu,fri],1)
    #print(schedule)


    #schedule(行列)をデータフレームに変換
        data_df = pd.DataFrame(schedule,
                        columns=['月2','月昼','月3','月4','月5','火2','火昼','火3','火4','火5','水2','水昼','水3','水4','水5','木2','木昼','木3','木4','木5','金2','金昼','金3','金4','金5'])


    #昼休みのみの人は、授業の空きコマを0とし、授業のみの人は、昼休みの空きコマを0とする。
        def lunch_only(lunch_num):
            all_index = []
            for each_index in data_df.index:
                all_index.append(each_index)
            all_index_iter = iter(all_index)
            for row in df.values:
                l = str(row[lunch_num])
                not_lunch_periods = ['月2','月3','月4','月5','火2','火3','火4','火5','水2','水3','水4','水5','木2','木3','木4','木5','金2','金3','金4','金5']
                index_num = next(all_index_iter)
                lunch_periods = ['月昼','火昼','水昼','木昼','金昼']
                if '昼休み / Lunch Break' in l:
                    for x in not_lunch_periods:
                        data_df.at[index_num,x] = 0
                elif '授業の空きコマ / Empty class period' in l:
                    for x in lunch_periods:
                        data_df.at[index_num,x] = 0
                else:
                    continue
            return data_df


    #data_dfを更新。
        data_df = lunch_only(20)
    #print(data_df)

    #1番右に全曜日の空きコマの合計の列を追加
        data_df = data_df.assign(合計 = data_df.sum(axis=1))

    #1番右にタイプ（日本人か留学生か）の列を追加
        data_df['タイプ'] = separate_group(8,10)

    #1番右にペアかグループかの列を追加
        data_df['ペア'] = pair_or_group(14)

    #1番右に性別の列を追加
        data_df['性別'] = gender(4)

    #1番右に国（中国かその他か）の列を追加
    #data_df['国'] = country(8)

    ##print(data_df)


    #空きコマがない人をpick up
        no_name = data_df[data_df['合計'] == 0]

        df.columns = list(range(len(df.columns)))
    #初期データから空きコマのない人のデータを消去。
        df_full = df.drop(no_name.index)
    #print(df_full)

    #print(df.at[56,2])
        print('空きコマがない人')
    #空きコマがない人を表示する。name_numは名前の列番号。
        def print_no_name(name_num):
            for i in no_name.index:
                print(i,':',df.at[i,name_num])

        print(print_no_name(2))
        

    #空きコマがないデータを排除
        data_full = data_df[data_df['合計'] > 0]


    #第一希望が特別な人を表示する。first_choice_numは第一希望の列番号。
        def first_choice(first_choice_num,name_num):
            all_index = []
            for each_index in data_full.index:
                all_index.append(each_index)
            all_index_iter = iter(all_index)
            for row in df_full.values:
                index_num = next(all_index_iter)
                c = str(row[first_choice_num])
                if 'Japanese' in c or 'English' in c:
                    continue
                else:
                    print(index_num,':',row[name_num])

        print()
        print('第一希望が特別な人')
        first_choice(12,2)


        pair = data_full[data_full['ペア'] == 1]
        both = data_full[data_full['ペア'] == 3]
    #print(pair)
    #print(both)


        pair_Jap = pair[pair['タイプ'] == 1]
        pair_Eng = pair[pair['タイプ'] == 2]
        pair_not_Eng = pair[pair['タイプ'] == 3]
        both_Eng = both[both['タイプ'] == 2]
        both_Jap = both[both['タイプ'] == 1]

    #print(pair_Eng)


    #ペアの相手がいない人を削除
        data_full = data_full.drop(pair_not_Eng.index)


        count_pair_Jap = pair_Jap.shape[0]
        count_pair_Eng = pair_Eng.shape[0]
        gap = count_pair_Jap - count_pair_Eng
    #print(count_pair_Eng)
    #print(count_pair_Jap)
        count_both_Eng = both_Eng.shape[0]
    #print(count_both_Eng)


        un = count_pair_Eng + count_both_Eng - count_pair_Jap 
        if un < 0:
            print('ペアを組める留学生が足りません。')
            sys.exit()

    #ペアを表示する。
        def print_pair_group(name_num,what_index):
            for i in what_index.index:
                print(i,':',df.at[i,name_num])

        print('以下からペア')

    #print(pair_Jap)
    #print(pair_Eng)

        man = data_df[data_df['性別'] == 2]
        woman = data_df[data_df['性別'] == 1]
        count_man = man.shape[0]
        count_woman = woman.shape[0]

    #print(man)
    #print(count_man)
    #print(count_woman)





    #日本人のペア希望の方が多い場合。どちらでもからpick up
        if gap > 0:
            both_Eng_sort = both_Eng.sort_values(by = ['性別', '合計'])

            for_pair_Eng = both_Eng_sort[0:gap]
        #print(for_pair_Eng)


            pair_Eng_2 = pd.concat([pair_Eng,for_pair_Eng])
            pair_Jap_sort = pair_Jap.sort_values(by = ['性別', '合計'])
            pair_Eng_2_sort = pair_Eng_2.sort_values(by = ['性別', '合計'])
        #print(pair_Jap_sort)
        #print(pair_Eng_2_sort)

            for i in range(count_pair_Jap):
                row_pair = pair_Jap_sort.head(1)
                for x in range(count_pair_Jap):
                    u_e = pd.DataFrame(pair_Eng_2_sort.iloc[x])
                    s_e = u_e.T
                    pd_pair = pd.concat([row_pair,s_e])
                    if pd_pair['月2'].sum() == 2 or pd_pair['月昼'].sum() == 2 or pd_pair['月3'].sum() == 2 or pd_pair['月4'].sum() == 2 or pd_pair['月5'].sum() == 2 or pd_pair['火2'].sum() == 2 or pd_pair['火昼'].sum() == 2 or pd_pair['火3'].sum() == 2 or pd_pair['火4'].sum() == 2 or pd_pair['火5'].sum() == 2 or pd_pair['水2'].sum() == 2 or pd_pair['水昼'].sum() == 2 or pd_pair['水3'].sum() == 2 or pd_pair['水4'].sum() == 2 or pd_pair['水5'].sum() == 2 or pd_pair['木2'].sum() == 2 or pd_pair['木昼'].sum() == 2 or pd_pair['木3'].sum() == 2 or pd_pair['木4'].sum() == 2 or pd_pair['木5'].sum() == 2 or pd_pair['金2'].sum() == 2 or pd_pair['金昼'].sum() == 2 or pd_pair['金3'].sum() == 2 or pd_pair['金4'].sum() == 2 or pd_pair['金5'].sum() == 2:
                    #print(pd_pair)
                    #関数print_pair(name_num,what_index)を使用。以下同様。
                        print()
                        print_pair_group(2,pd_pair)
                        data_full = data_full.drop(pd_pair.index)
                        pair_Jap_sort = pair_Jap_sort.drop(row_pair.index)
                        pair_Eng_2_sort = pair_Eng_2_sort.drop(s_e.index)
                        matching_date_pair = pd_pair.columns[pd_pair.sum(axis=0) == 2]
                        print(matching_date_pair)
                        print()
                        break
                    else:
                        continue
            if pair_Jap_sort.empty == True and pair_Eng_2_sort.empty == True:
                print('pair is over')
            else:
                print_pair_group(2,pair_Jap_sort)
                print_pair_group(2,pair_Eng_2_sort)
            #print(pair_Jap_sort)
            #print(pair_Eng_2_sort)        

    #留学生のペア希望の方が多い場合。どちらでもからpick up
        elif gap < 0:
        #man_pair_Jap = pair_Jap[pair_Jap['性別'] == 2]
        #woman_pair_Jap = pair_Jap[pair_Jap['性別'] == 1]
        #man_pair_Eng = pair_Eng[pair_Eng['性別'] == 2]
        #woman_pair_Eng = pair_Eng[pair_Eng['性別'] == 1]

        #man_pair_Jap_num = man_pair_Jap.shape[0]
        #woman_pair_Jap_num = woman_pair_Jap.shape[0]
        #man_pair_Eng_num = man_pair_Eng.shape[0]
        #woman_pair_Eng_num = woman_pair_Eng.shape[0]


        #print(man_pair_Eng_num)






            gap_2 = -1 * gap
            for_pair_Jap = both_Jap.sample(gap_2)
            pair_Jap_2 = pd.concat([pair_Jap,for_pair_Jap])
            pair_Jap_2_sort = pair_Jap_2.sort_values(by = ['性別', '合計'])
            pair_Eng_sort = pair_Eng.sort_values(by = ['性別', '合計'])
            for i in range(count_pair_Eng):
                row_pair = pair_Jap_2_sort.head(1)
                for x in range(count_pair_Eng):
                    u_e = pd.DataFrame(pair_Eng_sort.iloc[x])
                    s_e = u_e.T
                    pd_pair = pd.concat([row_pair,s_e])
                    if pd_pair['月2'].sum() == 2 or pd_pair['月昼'].sum() == 2 or pd_pair['月3'].sum() == 2 or pd_pair['月4'].sum() == 2 or pd_pair['月5'].sum() == 2 or pd_pair['火2'].sum() == 2 or pd_pair['火昼'].sum() == 2 or pd_pair['火3'].sum() == 2 or pd_pair['火4'].sum() == 2 or pd_pair['火5'].sum() == 2 or pd_pair['水2'].sum() == 2 or pd_pair['水昼'].sum() == 2 or pd_pair['水3'].sum() == 2 or pd_pair['水4'].sum() == 2 or pd_pair['水5'].sum() == 2 or pd_pair['木2'].sum() == 2 or pd_pair['木昼'].sum() == 2 or pd_pair['木3'].sum() == 2 or pd_pair['木4'].sum() == 2 or pd_pair['木5'].sum() == 2 or pd_pair['金2'].sum() == 2 or pd_pair['金昼'].sum() == 2 or pd_pair['金3'].sum() == 2 or pd_pair['金4'].sum() == 2 or pd_pair['金5'].sum() == 2:
                        print()
                        print_pair_group(2,pd_pair)
                    #print(pd_pair)
                        data_full = data_full.drop(pd_pair.index)
                        pair_Jap_2_sort = pair_Jap_2_sort.drop(row_pair.index)
                        pair_Eng_sort = pair_Eng_sort.drop(s_e.index)
                        matching_date_pair = pd_pair.columns[pd_pair.sum(axis=0) == 2]
                        print(matching_date_pair)
                        print()
                        break
                    else:
                        continue
            if pair_Jap_2_sort.empty == True and pair_Eng_sort.empty == True:
                print('pair is over')
            else:
                print_pair_group(2,pair_Jap_2_sort)
                print_pair_group(2,pair_Eng_sort)
            #print(pair_Jap_2_sort)
            #print(pair_Eng_sort)            

    #同数の場合。
        else:
            pair_Jap_sort = pair_Jap.sort_values(by = ['性別', '合計'])
            pair_Eng_sort = pair_Eng.sort_values(by = ['性別', '合計'])
            for i in range(count_pair_Jap):
                row_pair = pair_Jap_sort.head(1)
                for x in range(count_pair_Jap):
                    u_e = pd.DataFrame(pair_Eng_sort.iloc[x])
                    s_e = u_e.T
                    pd_pair = pd.concat([row_pair,s_e])
                    if pd_pair['月2'].sum() == 2 or pd_pair['月昼'].sum() == 2 or pd_pair['月3'].sum() == 2 or pd_pair['月4'].sum() == 2 or pd_pair['月5'].sum() == 2 or pd_pair['火2'].sum() == 2 or pd_pair['火昼'].sum() == 2 or pd_pair['火3'].sum() == 2 or pd_pair['火4'].sum() == 2 or pd_pair['火5'].sum() == 2 or pd_pair['水2'].sum() == 2 or pd_pair['水昼'].sum() == 2 or pd_pair['水3'].sum() == 2 or pd_pair['水4'].sum() == 2 or pd_pair['水5'].sum() == 2 or pd_pair['木2'].sum() == 2 or pd_pair['木昼'].sum() == 2 or pd_pair['木3'].sum() == 2 or pd_pair['木4'].sum() == 2 or pd_pair['木5'].sum() == 2 or pd_pair['金2'].sum() == 2 or pd_pair['金昼'].sum() == 2 or pd_pair['金3'].sum() == 2 or pd_pair['金4'].sum() == 2 or pd_pair['金5'].sum() == 2:
                        print()
                        print_pair_group(2,pd_pair)
                    #print(pd_pair)
                        data_full = data_full.drop(pd_pair.index)
                        pair_Jap_sort = pair_Jap_sort.drop(row_pair.index)
                        pair_Eng_sort = pair_Eng_sort.drop(s_e.index)
                        matching_date_pair = pd_pair.columns[pd_pair.sum(axis=0) == 2]
                        print(matching_date_pair)
                        print()
                        break
                    else:
                        continue
            if pair_Jap_sort.empty == True and pair_Eng_sort.empty == True:
                print('pair is over')
            else:
                print_pair_group(2,pair_Jap_sort)
                print_pair_group(2,pair_Eng_sort)
            #print(pair_Jap_sort)
            #print(pair_Eng_sort)



    #print(data_full)
    #print(df_full)

        Jap = data_full[data_full['タイプ'] == 1]
        Eng = data_full[data_full['タイプ'] == 2]
        not_Eng = data_full[data_full['タイプ'] == 3]

        Jap_sort = Jap.sort_values(by = ['合計'])
        Eng_sort = Eng.sort_values(by = ['合計'])
        not_Eng_sort = not_Eng.sort_values(by = ['合計'])


        #print('日本語の方が得意な留学生を含むグループ')
        #英語が話せない留学生が1人入るグループを作る。
        count_not_Eng = not_Eng_sort.shape[0]
        for i in range(count_not_Eng):
            row1 = not_Eng_sort.head(1)
            all_comb = itertools.combinations(Jap_sort.index,2)
            for first_group in all_comb:   
                first_group_list = list(first_group)
                u_2 = pd.DataFrame(Jap_sort.loc[first_group_list[0]])
                s_2 = u_2.T
                pd_group_2 = pd.concat([row1,s_2])
                u_3 = pd.DataFrame(Jap_sort.loc[first_group_list[1]])
                s_3 = u_3.T
                pd_group_3 = pd.concat([pd_group_2,s_3])

                if pd_group_3['月2'].sum() == 3 or pd_group_3['月昼'].sum() == 3 or pd_group_3['月3'].sum() == 3 or pd_group_3['月4'].sum() == 3 or pd_group_3['月5'].sum() == 3 or pd_group_3['火2'].sum() == 3 or pd_group_3['火昼'].sum() == 3 or pd_group_3['火3'].sum() == 3 or pd_group_3['火4'].sum() == 3 or pd_group_3['火5'].sum() == 3 or pd_group_3['水2'].sum() == 3 or pd_group_3['水昼'].sum() == 3 or pd_group_3['水3'].sum() == 3 or pd_group_3['水4'].sum() == 3 or pd_group_3['水5'].sum() == 3 or pd_group_3['木2'].sum() == 3 or pd_group_3['木昼'].sum() == 3 or pd_group_3['木3'].sum() == 3 or pd_group_3['木4'].sum() == 3 or pd_group_3['木5'].sum() == 3 or pd_group_3['金2'].sum() == 3 or pd_group_3['金昼'].sum() == 3 or pd_group_3['金3'].sum() == 3 or pd_group_3['金4'].sum() == 3 or pd_group_3['金5'].sum() == 3 :
                    not_Eng_sort = not_Eng_sort.drop(row1.index)
                    Jap_sort = Jap_sort.drop(s_2.index)
                    Jap_sort = Jap_sort.drop(s_3.index)
                    count_Eng = Eng_sort.shape[0]
                    for i in range(count_Eng):
                        u_4 = pd.DataFrame(Eng_sort.iloc[i])
                        s_4 = u_4.T
                        pd_group_4 = pd.concat([pd_group_3,s_4])
                    #print(pd_group_4)
                        if pd_group_4['月2'].sum() == 4 or pd_group_4['月昼'].sum() == 4 or pd_group_4['月3'].sum() == 4 or pd_group_4['月4'].sum() == 4 or pd_group_4['月5'].sum() == 4 or pd_group_4['火2'].sum() == 4 or pd_group_4['火昼'].sum() == 4 or pd_group_4['火3'].sum() == 4 or pd_group_4['火4'].sum() == 4 or pd_group_4['火5'].sum() == 4 or pd_group_4['水2'].sum() == 4 or pd_group_4['水昼'].sum() == 4 or pd_group_4['水3'].sum() == 4 or pd_group_4['水4'].sum() == 4 or pd_group_4['水5'].sum() == 4 or pd_group_4['木2'].sum() == 4 or pd_group_4['木昼'].sum() == 4 or pd_group_4['木3'].sum() == 4 or pd_group_4['木4'].sum() == 4 or pd_group_4['木5'].sum() == 4 or pd_group_4['金2'].sum() == 4 or pd_group_4['金昼'].sum() == 4 or pd_group_4['金3'].sum() == 4 or pd_group_4['金4'].sum() == 4 or pd_group_4['金5'].sum() == 4 :
                            #print(pd_group_4)
                            #関数print_pair_group(2,pair_Jap_sort)を使用。
                            print()
                            print_pair_group(2,pd_group_4)
                            Eng_sort = Eng_sort.drop(s_4.index)
                            matching_date = pd_group_4.columns[pd_group_4.sum(axis=0) == 4]
                            print(matching_date)
                            print()
                            break
                        else:
                            continue
                    break
                else :
                    continue 
        #print(Eng_sort)

        Jap_Eng = pd.concat([Jap_sort,Eng_sort])




        def under_n_periods(free_period_num): 
            pick_up_data = Jap_Eng[Jap_Eng['合計'] == free_period_num]
            selected_data = []
            for i in pick_up_data.index:
                under_n_list = pick_up_data.columns[pick_up_data.loc[i] > 0].tolist()
                under_n_list.remove('合計')
                under_n_list.remove('タイプ')
                under_n_list.remove('ペア')
                selected_data.append(random.choice(under_n_list))
            set_under_n = set(selected_data)
            final_under_n = list(set_under_n)
            return final_under_n


        free_period_1 = under_n_periods(1)
        free_period_2 = under_n_periods(2)
        free_period_3 = under_n_periods(3)
        #print(free_period_1)
        #print(free_period_2)
        #print(free_period_3)




        def priority_period(period):
            Jap_2 = Jap_Eng[Jap_Eng['タイプ'] == 1]
            Eng_2 = Jap_Eng[Jap_Eng['タイプ'] == 2]
            Jap_sort_new = Jap_2.sort_values(by=[period,'合計'], ascending=[False, True])
            Eng_sort_new = Eng_2.sort_values(by=[period,'合計'], ascending=[False, True])
        #print(data_sort)
            all_comb_Jap = itertools.combinations(Jap_sort_new.index,2)
            first_group_j = next(all_comb_Jap)
            group_j = []
            for i in range(2):
                group_j.append(Jap_sort_new.loc[first_group_j[i],period])
            if sum(group_j) == 2:
                for i in range(2):
                    Jap_sort_new = Jap_sort_new.drop(first_group_j[i])
                #print(first_group)
                all_comb_Eng = itertools.combinations(Eng_sort_new.index,2)
                first_group_e = next(all_comb_Eng)
                group_e = []
                for i in range(2):
                    group_e.append(Eng_sort_new.loc[first_group_e[i],period])
                if sum(group_e) == 2:
                    for i in range(2):
                        Eng_sort_new = Eng_sort_new.drop(first_group_e[i])
                    #print(first_group_j)
                    #print(first_group_e)
                    first_group_j_list = list(first_group_j)
                    first_group_e_list = list(first_group_e)
                    j_1 = pd.DataFrame(Jap_Eng.loc[first_group_j_list[0]])
                    j_1_t = j_1.T
                    j_2 = pd.DataFrame(Jap_Eng.loc[first_group_j_list[1]])
                    j_2_t = j_2.T
                    e_1 = pd.DataFrame(Jap_Eng.loc[first_group_e_list[0]])
                    e_1_t = e_1.T
                    e_2 = pd.DataFrame(Jap_Eng.loc[first_group_e_list[1]])
                    e_2_t = e_2.T
                    create_group = pd.concat([j_1_t,j_2_t,e_1_t,e_2_t])
                    #関数print_pair_group(2,pair_Jap_sort)を使用。
                    print()
                    print_pair_group(2,create_group)
                    #print(create_group)            
                    matching_date_2 = create_group.columns[create_group.sum(axis=0) == 4]
                    print(matching_date_2)
                    print()
                    Jap_Eng_new = pd.concat([Jap_sort_new,Eng_sort_new])
                    return Jap_Eng_new
                else:
                    return Jap_Eng
            else:
                #print(data_sort)
                return Jap_Eng


        def priority_period_cycle(period):    
            Jap_2 = Jap_Eng[Jap_Eng['タイプ'] == 1]
            Eng_2 = Jap_Eng[Jap_Eng['タイプ'] == 2]
            Jap_sort_new = Jap_2.sort_values(by=[period,'合計'], ascending=[False, True])
            Eng_sort_new = Eng_2.sort_values(by=[period,'合計'], ascending=[False, True])
        #print(data_sort)
            
            for i in range(1000000):
                try:
                    all_comb_Jap = itertools.combinations(Jap_sort_new.index,2)
                    first_group_j = next(all_comb_Jap)
                    group_j = []
                    for i in range(2):
                        group_j.append(Jap_sort_new.loc[first_group_j[i],period])
                    if sum(group_j) == 2:
                        #print(first_group)
                        all_comb_Eng = itertools.combinations(Eng_sort_new.index,2)
                        first_group_e = next(all_comb_Eng)
                        group_e = []
                        for i in range(2):
                            group_e.append(Eng_sort_new.loc[first_group_e[i],period])
                        if sum(group_e) == 2:
                            for i in range(2):
                                #print(Jap_sort_new)
                                Jap_sort_new = Jap_sort_new.drop(first_group_j[i])
                            for i in range(2):
                                Eng_sort_new = Eng_sort_new.drop(first_group_e[i])
                    #print(first_group_j)
                    #print(first_group_e)
                            first_group_j_list = list(first_group_j)
                            first_group_e_list = list(first_group_e)
                            j_1 = pd.DataFrame(Jap_Eng.loc[first_group_j_list[0]])
                            j_1_t = j_1.T
                            j_2 = pd.DataFrame(Jap_Eng.loc[first_group_j_list[1]])
                            j_2_t = j_2.T
                            e_1 = pd.DataFrame(Jap_Eng.loc[first_group_e_list[0]])
                            e_1_t = e_1.T
                            e_2 = pd.DataFrame(Jap_Eng.loc[first_group_e_list[1]])
                            e_2_t = e_2.T
                            create_group = pd.concat([j_1_t,j_2_t,e_1_t,e_2_t])
                            #関数print_pair_group(2,pair_Jap_sort)を使用。
                            print()
                            print_pair_group(2,create_group)
                            #print(create_group)            
                            matching_date_2 = create_group.columns[create_group.sum(axis=0) == 4]
                            print(matching_date_2)
                            print()
                            Jap_Eng_new = pd.concat([Jap_sort_new,Eng_sort_new])                    
                        else:
                            #print(Jap_Eng_new)
                            #print(Jap_Eng_new)                    
                            Jap_Eng_new = pd.concat([Jap_sort_new,Eng_sort_new])
                            #print(Jap_Eng_new)
                            return Jap_Eng_new
                            break
                    else:
                        #print(Jap_sort_new)
                        #print(Eng_sort_new)
                        Jap_Eng_new = pd.concat([Jap_sort_new,Eng_sort_new])
                        #print(Jap_Eng_new)
                        return Jap_Eng_new
                        break
                except StopIteration:
                    #print(Jap_sort_new)
                    #print(Eng_sort_new)
                    Jap_Eng_new = pd.concat([Jap_sort_new,Eng_sort_new])
                    print()
                    print('あまった人')
                    print_pair_group(2,Jap_Eng_new)
                    print(Jap_Eng_new)
                    print('All MISSION COMPLETE')
                    break
                #except TypeError:
                    #print('All MISSION COMPLETE')


        random.shuffle(free_period_1)
        iter_free_periods_1 = iter(free_period_1)
        for i in range(25):
            try:
                what_period_1 = next(iter_free_periods_1)
                #print(what_period_1)
                Jap_Eng = priority_period(what_period_1)        
            except StopIteration:
                #print(data_full)
                #print('First mission complete')
                break






        random.shuffle(free_period_2)
        iter_free_periods_2 = iter(free_period_2)
        for i in range(25):
            try:
                what_period_2 = next(iter_free_periods_2)
                #print(what_period_2)
                Jap_Eng = priority_period(what_period_2)
            except StopIteration:
                #print(data_full)
                #print('Second mission complete')
                break

        random.shuffle(free_period_3)
        iter_free_periods_3 = iter(free_period_3)
        for i in range(25):
            try:
                what_period_3 = next(iter_free_periods_3)
                #print(what_period_3)
                Jap_Eng = priority_period(what_period_3)
            except StopIteration:
                #print(data_full)
                break


        free_periods = ['月2','月昼','月3','月4','月5','火2','火昼','火3','火4','火5','水2','水昼','水3','水4','水5','木2','木昼','木3','木4','木5','金2','金昼','金3','金4','金5']
        random.shuffle(free_periods)
        iter_free_periods = iter(free_periods)
        for i in range(26):
            try:
                what_period = next(iter_free_periods)
                Jap_Eng = priority_period_cycle(what_period)
                #print(data_full)
            except StopIteration:
                print()
                print('あまった人')
                print_pair_group(2,Jap_Eng)
                print(Jap_Eng)
                print('All mission complete')
                print()
                break
            except TypeError:
                break


        print()
        print('ペアの相手がいない')
        print_pair_group(2,pair_not_Eng)
        print()



        print()
        print('重複している可能性あり')
        duplication = df_full[df_full.duplicated(subset = 22)]
        print_pair_group(2,duplication)

        output = buffer.getvalue()
    finally:
         sys.stdout = sys_stdout  # 標準出力を元に戻す

    return output  # ← これが Flask の画面に表示される