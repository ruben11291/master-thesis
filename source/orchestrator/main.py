 #!/usr/bin/env python

if __name__ == "__main__":
    import sys
    import orchestator
    from orchestator import orchestator,Iorchestator
    import listener
    from listener import listener
    print "NADA"

    orch =  orchestator()
    lst = listener( orch )
    lst.pooling()
