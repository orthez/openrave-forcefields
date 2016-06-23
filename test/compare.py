import numpy as np
import matplotlib.pyplot as plt


X1=np.array( [[-2.0, -2.0008503593297324, -2.0018138850292293, -2.002890577098489, -2.004080435537513, -2.0053834603462994, -2.00679965152485, -2.0083290090731643, -2.009971532991242, -2.0117272232790837, -2.013596079936689, -2.0155781029640574, -2.0176732923611898, -2.0198816481280857, -2.0222031702647456, -2.024637858771168, -2.027185713647355, -2.029846734893305, -2.032620922509019, -2.0355082764944967, -2.0385087968497375, -2.0416224835747427, -2.0448493366695106, -2.0481893561340425, -2.0516425419683384, -2.0552088941723974, -2.05888841274622, -2.0626810976898065, -2.066586949003156, -2.0706059666862693, -2.074738150739147, -2.0789835011617877, -2.083342017954192, -2.0878137011163598, -2.0923985506482907, -2.097096566549986, -2.101907748821445, -2.106832097462667, -2.1888773508359285, -2.2037372338601746, -2.21544067309819, -2.2234668679093232, -2.227533621647433, -2.2275978141366375, -2.2238462240062016, -2.216677238925571, -2.2066742888769886, -2.194572105710574, -2.1812171435884458, -2.1616151003778254, -2.148272164067175, -2.136194890479416, -2.1262281264631566, -2.1191042455161173, -2.1154036727278673, -2.1155212780118258, -2.119639967573437, -2.1277125713200857, -2.1394528550993575, -2.154336189034964, -2.2513260342655346, -2.2589663757810827, -2.2667198836663953, -2.2745865579214715, -2.282566398546311, -2.2906594055409135, -2.2988655789052808, -2.307184918639411, -2.315617424743305, -2.3241630972169625, -2.3328219360603835, -2.3415939412735685, -2.350479112856517, -2.3594774508092287, -2.3685889551317043, -2.3778136258239435, -2.387151462885946, -2.3966024663177126, -2.4061666361192424, -2.4158439722905363, -2.425634474831593, -2.4355381437424137, -2.4455549790229982, -2.4556849806733463, -2.4659281486934574, -2.476284483083333, -2.4867539838429717, -2.497336650972374, -2.5080324844715394, -2.518841484340469, -2.529763650579163, -2.54079898318762, -2.5519474821658394, -2.563209147513824, -2.574583979231571, -2.5860719773190826, -2.5976731417763568, -2.6093874726033954, -2.6212149698001976, -2.633155633366763], [1.3469636304139304e-20, 5.381768415959414e-06, 1.0470012126950253e-05, 1.526473113297253e-05, 1.9765925434026243e-05, 2.3973595030111394e-05, 2.788773992122799e-05, 3.150836010737601e-05, 3.483545558855548e-05, 3.786902636476638e-05, 4.060907243600873e-05, 4.30555938022825e-05, 4.520859046358771e-05, 4.7068062419924377e-05, 4.863400967129246e-05, 4.9906432217691975e-05, 5.088533005912296e-05, 5.1570703195585355e-05, 5.19625516270792e-05, 5.206087535360447e-05, 5.18656743751612e-05, 5.1376948691749376e-05, 5.059469830336896e-05, 4.951892321001999e-05, 4.814962341170247e-05, 4.6486798908416366e-05, 4.453044970016171e-05, 4.228057578693851e-05, 3.973717716874672e-05, 3.690025384558636e-05, 3.376980581745745e-05, 3.034583308435997e-05, 2.662833564629395e-05, 2.261731350325938e-05, 1.8312766655256162e-05, 1.37146951022845e-05, 8.823098844344202e-06, 3.6379778814353515e-06, -0.0018117915243418504, -0.00785643182279266, -0.01733068122080779, -0.029251241189729913, -0.04258185226532921, -0.056283537423786126, -0.06936329859815168, -0.08091953029280823, -0.09018254845221761, -0.09654881577298832, -0.0996076707583074, -0.09956946328829297, -0.09645856989336228, -0.09004517300252714, -0.08074323072469135, -0.06915913998267402, -0.05606485336888368, -0.04236352256292421, -0.029048866205721786, -0.01715968533113978, -0.007731131442239976, -0.0017444653589215329, -0.0001966326228367911, -0.00020886233671894538, -0.00022138557530606843, -0.00023420233859815982, -0.0002473126265952198, -0.0002607164392972484, -0.00027441377670424545, -0.0002884046388162112, -0.00030268902563314565, -0.00031726693715504836, -0.0003321383733819196, -0.0003473033343137597, -0.00036276181995056824, -0.0003785138302923453, -0.00039455936533909085, -0.00041089842509080526, -0.0004275310095474879, -0.0004444571187091393, -0.00046167675257575915, -0.00047918991114734766, -0.0004969965944239045, -0.0005150968024054301, -0.0005334905350919244, -0.000552177792483387, -0.0005711585745798182, -0.000590432881381218, -0.0006100007128875864, -0.0006298620690989234, -0.0006500169500152289, -0.000670465355636503, -0.0006912072859627457, -0.0007122427409939569, -0.0007335717207301365, -0.0007551942251712849, -0.0007771102543174019, -0.0007993198081684876, -0.0008218228867245414, -0.0008446194899855639, -0.000867709617951555, -0.0008910932706225148]] )
X2=np.array( [[-2.0, -2.0007724331609675, -2.0016393249236977, -2.0026006752881904, -2.0036564842544444, -2.0048067518224606, -2.0060514779922407, -2.0073906627637834, -2.008824306137087, -2.0103524081121544, -2.011974968688983, -2.0136919878675745, -2.015503465647928, -2.017409402030044, -2.0194097970139224, -2.0215046505995637, -2.0236939627869672, -2.0259777335761338, -2.028355962967061, -2.030828650959751, -2.033395797554205, -2.036057402750421, -2.0388134665483975, -2.04166398894814, -2.0446089699496506, -2.0476484095528016, -2.0507823077587264, -2.0540106645596534, -2.057333480001923, -2.060750753842502, -2.064262487225627, -2.067868675138733, -2.071569338059031, -2.075364401056776, -2.0792540802576305, -2.0832381784757286, -2.08731295354168, -2.0915211420951247, -2.0955358945724494, -2.10145783510402, -2.0974051117371655, -2.142521098448434, -2.201617796380842, -2.2062776829318422, -2.2175045926853025, -2.2241057986187425, -2.227586921797981, -2.227704432637892, -2.2246189494751616, -2.21861686752877, -2.2101458982609747, -2.199575802353674, -2.188404106660518, -2.1731217402669296, -2.156459251943138, -2.145218393842681, -2.134405190461768, -2.1255825331290925, -2.1191617693805695, -2.115599295861349, -2.1151968068382656, -2.1181757306408797, -2.1241540330086566, -2.1351922610208725, -2.1396970534933235, -2.1890539799323188, -2.262516339948437, -2.2592834165687767, -2.2678594870819775, -2.2748880786270234, -2.282185591590518, -2.289573600453345, -2.2970509933027605, -2.3046249255582785, -2.312292713549137, -2.3200551123188755, -2.3279119341400833, -2.335863222353362, -2.343908967615604, -2.352049171750821, -2.3602838344461294, -2.368612955748542, -2.3770365356522767, -2.385554574157738, -2.3941670712649925, -2.4028740269740005, -2.411675441284772, -2.4205713141973058, -2.4295616457116016, -2.43864643582766, -2.4478256845454816, -2.4570993918650643, -2.46646755778641, -2.4759301823095186, -2.4854872654343887, -2.4951388071610223, -2.504884807489417, -2.514725266419576, -2.5246601839514966, -2.5346895600851793], [1.3417020537326259e-20, 4.928434415808495e-06, 9.611867306234752e-06, 1.4050298671278789e-05, 1.8243728510940587e-05, 2.2192156825220165e-05, 2.5895583614117525e-05, 2.9354008877632655e-05, 3.256743261576556e-05, 3.5535854828516245e-05, 3.825927551588469e-05, 4.073769467787093e-05, 4.297111231447493e-05, 4.495952842569669e-05, 4.6702943011536244e-05, 4.820135607199357e-05, 4.945476760706866e-05, 5.0463177616761544e-05, 5.122658610107224e-05, 5.1744993060000454e-05, 5.201839849354744e-05, 5.204680240170851e-05, 5.183020478449899e-05, 5.13686056418877e-05, 5.0662004973782607e-05, 4.971040278193463e-05, 4.851379905128176e-05, 4.7072193884957554e-05, 4.538558666798719e-05, 4.345398062564382e-05, 4.1277360572841893e-05, 3.885579303097872e-05, 3.618900624848838e-05, 3.327799461242977e-05, 3.011988993531566e-05, 2.671730905599151e-05, 2.3119914024584725e-05, 1.8760550092700202e-05, 1.797681337383978e-05, -7.108521859422705e-06, 0.00010118771300756306, -0.0004420217747075427, -0.0035649539382634635, -0.010248996244041325, -0.019532071939570475, -0.030696148452497893, -0.042939143654324254, -0.05546897114773938, -0.06752555485367578, -0.07841146992222728, -0.08751657718507316, -0.09435164653685596, -0.0985063821308846, -0.09996221057827866, -0.09887999418625174, -0.09516671785799087, -0.08872040115167383, -0.079937285821678, -0.06928936648453862, -0.05737119498161006, -0.044868586692571405, -0.03253400239026977, -0.021154478307859263, -0.011539101661302831, -0.004388749535053467, -0.0007260666180758514, -0.00012364592195860083, -0.00022280609533008758, -0.0002216290195055572, -0.00023479479648454496, -0.00024670761861818183, -0.00025889946646333317, -0.000271379887021557, -0.00028408744309693884, -0.00029704517697316324, -0.000310246605765795, -0.00032369334132241484, -0.00033738501151599914, -0.00035132169656746975, -0.00036550338081564983, -0.00037993006694701136, -0.00039460175455790077, -0.00040951844369793814, -0.0004246801343636618, -0.00044008682655451007, -0.0004557385202708273, -0.0004716352155125034, -0.00048777691227956747, -0.0005041636105720122, -0.0005207953103898396, -0.0005376720117330493, -0.0005547937146016409, -0.0005721604189956151, -0.0005897721249149712, -0.0006076288323597095, -0.0006257305413298302, -0.0006440772518253335, -0.0006626689638462186, -0.0006815056773924859, -0.0007005873924641355]] )



plt.plot(X1[0,:],X1[1,:],'-r')
plt.plot(X2[0,:],X2[1,:],'-b')
print np.linalg.norm(X1-X2)
plt.show()