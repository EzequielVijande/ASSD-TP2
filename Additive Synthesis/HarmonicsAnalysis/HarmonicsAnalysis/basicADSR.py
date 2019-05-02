import matplotlib.pyplot as plt
import additiveSynthesis as addsyn

def main():
    fs = 44100
    addsyn.adsrSynthGuitar(110,3)
    addsyn.adsrDesvSynthGuitar(110,3)
    addsyn.adsrSynthViolin(194,1.3)
    addsyn.adsrDesvSynthViolin(194,1.3)
    addsyn.adsrSynthSaxophone(110,3)
    addsyn.adsrDesvSynthSaxophone(110,3)
    addsyn.adsrSynthTrumpet(110,3)
    addsyn.adsrDesvSynthTrumpet(110,3)
    plt.show()

if __name__== "__main__":
  main()
