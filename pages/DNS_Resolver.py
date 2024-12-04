import dns.resolver
import streamlit as st
st.set_page_config(
   page_title="DNS Resolver",
   page_icon="🔍",
   layout="wide",
#    initial_sidebar_state="expanded",
)
def check_dns_records(domain):
    try:
        record_types = ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS', 'SOA']
        resolver = dns.resolver.Resolver()
        results = {}
        for record_type in record_types:
            try:
                answer = resolver.resolve(domain, record_type)
                results[record_type] = [str(rdata) for rdata in answer]
            except dns.resolver.NoAnswer:
                results[record_type] = []
            except dns.resolver.NXDOMAIN:
                results[record_type] = []
            except dns.resolver.NoNameservers:
                results[record_type] = []
            except Exception as e:
                results[record_type] = str(e)
        return results
    except Exception as e:
        return {'error': str(e)}
def display_results(domain, results):
    st.markdown("\n" + f":rainbow[DNS Records for {domain}]", unsafe_allow_html=False)
    st.markdown("=" * (len(f"DNS Records for {domain}") + 2), unsafe_allow_html=False)
    if 'error' in results:
        st.markdown(f":red[Error: {results['error']}]")
        return
    for record_type, record_data in results.items():
        if record_type == "A":
            record_title = "IPv4 Addresses"
        elif record_type == "AAAA":
            record_title = "IPv6 Addresses"
        elif record_type == "MX":
            record_title = "Mail Exchanger"
        elif record_type == "CNAME":
            record_title = "Canonical Name"
        elif record_type == "TXT":
            record_title = "Text Records"
        elif record_type == "NS":
            record_title = "Name Servers"
        elif record_type == "SOA":
            record_title = "Start of Authority"
        st.markdown(f"\n**<u>{record_title}:**</u>", unsafe_allow_html=True)
        if record_data:
            for record in record_data:
                st.markdown(f":green[- {record}]", unsafe_allow_html=False)
        else:
            st.markdown(":red[  - Not found]")
    st.write("=" * 40)
st.title("DNS Resolver")	
st.markdown("*Enter a domain to check its DNS records.*")
st.markdown("*The tool will check for A, AAAA, MX, CNAME, TXT, NS, and SOA records.*")

domain = st.text_input("Enter domain to check DNS records: ").strip()
if st.button("Check DNS Records", icon="😃", use_container_width=True):
    results = check_dns_records(domain)
    display_results(domain, results)