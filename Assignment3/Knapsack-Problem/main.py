import os
import time
import pandas as pd
from ortools.algorithms.python import knapsack_solver

def get_data(link):
    file_list = open(link, "r").read().split("\n") 
    capacities = []  
    capacities.append(int(file_list[2]))  
    values = []
    weights = [[]]
    for a in file_list[4:-1]:
        b = a.split(" ")
        values.append(int(b[0]))
        weights[0].append(int(b[1]))
    return values, weights, capacities

folderpath = './Knapsack-Problem/test-cases'

dict_group = {0: "00Uncorrelated", 1: "01WeaklyCorrelated", 2: "02StronglyCorrelated", 3: "03InverseStronglyCorrelated",
              4: "04AlmostStronglyCorrelated", 5: "05SubsetSum", 6: "06UncorrelatedWithSimilarWeights" ,
              7: "07SpannerUncorrelated" ,8: "08SpannerWeaklyCorrelated" ,9: "09SpannerStronglyCorrelated",
              10: "10MultipleStronglyCorrelated" , 11: "11ProfitCeiling" ,12: "12Circle"}

item_amount_folder = {50: "n00050", 100: "n00100", 200: "n00200", 500: "n00500",
                      1000: "n01000", 2000: "n02000"} 

def main():
    #case = 's000.kp'
    #case = 's019.kp'
    case = 's085.kp'

    computed_value_table = []   # Bảng chứa giá trị value đã được tính toán trong thời gian tối đa
    total_weight_table = []     # Bảng chứa giá trị total weight cho lời giải tốt nhất
    optimal_table = []      # Bảng đánh giá kết quả có tối ưu hay không
    list_size = []     # Danh sách các kích thước được sử dụng, để tạo thông tin cột cho table
    list_name = []     # Danh sách tên thư mục được sử dụng, để tạo cột header cho table

    solver = knapsack_solver.KnapsackSolver(
    knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
    "KnapsackExample",
    )

    time_limit = 180    # thời gian thực nghiệm để đánh giá tối ưu

    # list các nhóm test case được sử dụng
    for group in dict_group:
        list_name.append(dict_group[group])  
        
    for item in item_amount_folder:
        computed_value_list = []
        total_weight_list = []
        list_optimal = []
        list_size.append(item)
        
        for group in dict_group:
            path = os.path.join(folderpath, dict_group[group], item_amount_folder[item], "R01000", case) 
            values, weights, capacities = get_data(path) 
            solver.init(values, weights, capacities)
            solver.set_time_limit(time_limit)
            t0 = time.time()            # thời gian lúc chuẩn bị chạy thuật toán  
            computed_value = solver.solve()   # Giải quyết bài toán
            t1 = time.time() - t0       #  t1 là hiệu thời gian lúc chưa chạy và sau khi chạy thuật toán
            optimal = True              # trả về kết trả tối ưu hay chưa
            if t1 >= time_limit:   # nếu thời gian chạy > thời gian tối đa, trả về False
                optimal = False
            packed_items = []   
            packed_weights = []
            total_weight = 0
            
            for i in range(len(values)):
                if solver.best_solution_contains(i):
                    packed_items.append(i)
                    packed_weights.append(weights[0][i])
                    total_weight += weights[0][i]
            total_weight_list.append(total_weight)          
            computed_value_list.append(computed_value)         
            list_optimal.append(optimal)   
            print("Result for",path)
            print('Total weight:', total_weight)
            print('Packed items:', packed_items)
            print('Packed_weights:', packed_weights) 
                    
        computed_value_table.append(computed_value_list)               
        total_weight_table.append(total_weight_list)    
        optimal_table.append(list_optimal)     
        print("--------------------------------------")
        print("Case with", item, "items done")
        print("--------------------------------------")
    
    output_folder = './Knapsack-Problem/results'
    os.makedirs(output_folder, exist_ok=True)

    # Tạo DataFrame từ computed_value_table và lưu vào tệp computed_value_table.csv
    computed_value_table_df = pd.DataFrame(computed_value_table, columns=list_name)
    computed_value_table_df.insert(loc=0, column="testcases", value=list_size)   
    computed_value_table_df.to_csv(f'{output_folder}/computed_value_{case}_table.csv', index=False)   
       
    # Tạo DataFrame từ total_weight_table và lưu vào tệp total_weight_table.csv
    total_weight_table = pd.DataFrame(total_weight_table, columns=list_name)
    total_weight_table.insert(loc=0, column="testcases", value=list_size)
    total_weight_table.to_csv(f'{output_folder}/total_weight_{case}_table.csv', index=False)
    
    # Tạo DataFrame từ optimal_table và lưu vào tệp optimal_table.csv
    optimal_table_df = pd.DataFrame(optimal_table, columns=list_name)
    optimal_table_df.insert(loc=0, column="testcases", value=list_size)
    optimal_table_df.to_csv(f'{output_folder}/optimal_{case}_table.csv', index=False)

if __name__ == '__main__':
    main()
