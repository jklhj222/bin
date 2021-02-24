using CSV
using DataFrames
using Glob

log_ors_dir = "log_ors_20210114"
output_file = "PR_version101-240.dat"
#data_file = "epoch=95-val_loss=0.000-val_acc=1.000-data18_test_10000G_2207P_484I.csv"

function calc_confused_matrix(tgt, pred)
  G_tp = G_fp = G_fn = G_tn= 0
  I_tp = I_fp = I_fn = I_tn= 0
  P_tp = P_fp = P_fn = P_tn= 0

  for (t, p) in zip(tgt, pred)

    # calculation of G
    if p == "G"

      if t == "G"
        G_tp += 1
      else
        G_fp += 1
      end

    elseif p != "G"

      if t == "G"
        G_fn += 1
      else 
        G_tn += 1
      end

    end

    # calculation of I
    if p == "I"

      if t == "I"
        I_tp += 1
      else
        I_fp += 1
      end

    elseif p != "I"

      if t == "I"
        I_fn += 1
      else 
        I_tn += 1
      end

    end

    # calculation of P
    if p == "P"

      if t == "P"
        P_tp += 1
      else
        P_fp += 1
      end

    elseif p != "P"

      if t == "P"
        P_fn += 1
      else 
        P_tn += 1
      end

    end

  end

  G_precision = G_tp / (G_tp + G_fp)
  G_recall = G_tp / (G_tp + G_fn)

  I_precision = I_tp / (I_tp + I_fp)
  I_recall = I_tp / (I_tp + I_fn)

  P_precision = P_tp / (P_tp + P_fp)
  P_recall = P_tp / (P_tp + P_fn)

  PI_precision = (P_tp + I_tp) / (P_tp + P_fp + I_tp + I_fp)
  PI_recall = (P_tp + I_tp) / (P_tp + P_fn + I_tp + I_fn)

  tot_accuracy = (G_tp + I_tp + P_tp) / length(tgt)

  println("P_tp, P_fp, P_fn, P_tn")
  println((P_tp, P_fp, P_fn, P_tn))

  println("I_tp, I_fp, I_fn, I_tn")
  println((I_tp, I_fp, I_fn, I_tn))

  return tot_accuracy, G_precision, G_recall, I_precision, I_recall, P_precision, P_recall, PI_precision, PI_recall

end

f = open(output_file, "w")

for dir in readdir(log_ors_dir, join=true)
  println(dir)
  write(f, dir*"\n")

  log_files = glob(joinpath(dir, "*.csv"))

#  println(log_files, length(log_files))

  if length(log_files) > 0
    for log_file in log_files
      df = CSV.read(log_file, header=1, delim=',', DataFrame)
      tgt = df."target"
      pred = df."predict"

      pr = calc_confused_matrix(tgt, pred)

      println(log_file)
      println("Accuracy, G_precision, G_recall, I_precision, I_recall, P_precision, P_recall, PI_precision, PI_recall")
      println(pr)
      println()

      write(f, log_file * "\n")
      write(f, "Accuracy, G_precision, G_recall, I_precision, I_recall, P_precision, P_recall, PI_precision, PI_recall\n")
      write(f, string(pr) * "\n\n")
      
    end 
    
  end

end


#println("G_precision, G_recall, I_precision, I_recall, P_precision, P_recall")
#println(pr)

#for (t, p) in zip(tgt, pred)
#  if t == p
#    println(t, p)
#    println(typeof(t), typeof(p))
#  end
#end


#println(df, size(df))
#println(tgt, size(tgt))
#println(size(df[!, 15]))

#for acc in accs
#    println(acc)
#end
