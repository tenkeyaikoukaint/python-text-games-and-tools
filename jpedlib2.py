class jel:

    def __init__(self):

        self.chrmap={
            "  ":32,
            "xa":12354,"xi":12356,"xu":12358,"xe":12360,"xo":12362,
            "ka":12363,"ki":12365,"ku":12367,"ke":12369,"ko":12371,
            "sa":12373,"si":12375,"su":12377,"se":12379,"so":12381,
            "ta":12383,"ti":12385,"tu":12388,"te":12390,"to":12392,
            "na":12394,"ni":12395,"nu":12396,"ne":12397,"no":12398,
            "ha":12399,"hi":12402,"hu":12405,"he":12408,"ho":12411,
            "ma":12414,"mi":12415,"mu":12416,"me":12417,"mo":12418,
            "ya":12420,"yu":12422,"yo":12424,
            "ra":12425,"ri":12426,"ru":12427,"re":12428,"ro":12429,
            "wa":12431,"wo":12434,"nn":12435,"vu":12436,
            "ga":12364,"gi":12366,"gu":12368,"ge":12370,"go":12372,
            "za":12374,"zi":12376,"zu":12378,"ze":12380,"zo":12382,
            "da":12384,"di":12386,"du":12389,"de":12391,"do":12393,
            "ba":12400,"bi":12403,"bu":12406,"be":12409,"bo":12412,
            "pa":12401,"pi":12404,"pu":12407,"pe":12410,"po":12413,
            "ja":12419,"ju":12421,"jo":12423,"tt":12387,"hh":12540,
            "la":12353,"li":12355,"lu":12357,"le":12359,"lo":12361,
            "/jyo":12069,"/kod":12070,"/you":24188,"/dan":30007
        }

    def tojp(self,inp):
        stg=""
        mode="normal"
        for i in range(0,len(inp),2):
            if mode=="skip":
                mode="normal"
            elif inp[i:i+1]=="/":
                try:
                    stg=stg+chr(self.chrmap[inp[i:i+4]])
                except NameError and KeyError:
                    stg=stg+chr(12288)
                mode="skip"
            elif inp[i:i+1]=="e":
                stg=stg+inp[i+1]
            elif inp[i:i+1].isupper():
                char=inp[i:i+2].lower()
                if char!="hh":
                    try:
                       stg=stg+chr(self.chrmap[char]+96)
                    except NameError and KeyError:
                        stg=stg+chr(12288)
                else:
                    stg=stg+chr(self.chrmap[char])
            else:
                char=inp[i:i+2]
                try:
                    stg=stg+chr(self.chrmap[char])
                except NameError and KeyError:
                    stg=stg+chr(12288)
        return stg
