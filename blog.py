import modfsnif
from flask import Flask, render_template, url_for, jsonify, request
import config


app = Flask(__name__)
print ('hii from blog ******************************************************************')
print (config.F)
post=[{
                'EtdFdest_mac':config.F['EtdFdest_mac'],
                'EtdFsrc_mac':config.F['EtdFsrc_mac'],
                'EtdFdata':config.F['EtdFdata'],
                'EtdFetd_proto':config.F['EtdFetd_proto'],
                'version':config.F['version'],
                'header_lengtd':config.F['header_lengtd'],
                'ttl':config.F['ttl'],
                'src':config.F['src'],
                'target':config.F['target'],
                'type':config.F['type'],
                'ICMPtype':config.F['ICMPtype'],
                'ICMPcode':config.F['ICMPcode'],
                'ICMPchecksum':config.F['ICMPchecksum'],
                'TCPdestP':config.F['TCPdestP'],
                'TCPsrcP':config.F['TCPsrcP'],
},
{
                'EtdFdest_mac':config.F['EtdFdest_mac'],
                'EtdFsrc_mac':config.F['EtdFsrc_mac'],
                'EtdFdata':config.F['EtdFdata'],
                'EtdFetd_proto':config.F['EtdFetd_proto'],
                'version':config.F['version'],
                'header_lengtd':config.F['header_lengtd'],
                'ttl':config.F['ttl'],
                'src':config.F['src'],
                'target':config.F['target'],
                'type':config.F['type'],
                'ICMPtype':config.F['ICMPtype'],
                'ICMPcode':config.F['ICMPcode'],
                'ICMPchecksum':config.F['ICMPchecksum'],
                'TCPdestP':config.F['TCPdestP'],
                'TCPsrcP':config.F['TCPsrcP'],
}
]

@app.route("/")
@app.route("/home")
def home():
   return render_template('home.html', posts=post)

#@app.route("/dynamic")
#def dynamic():
#    return render_template('dynamic.html', posts=parent_dict) 

@app.route("/about")
def about():
    return render_template('about.html', title='About')




if __name__ == '__main__':
    app.run(debug=True)