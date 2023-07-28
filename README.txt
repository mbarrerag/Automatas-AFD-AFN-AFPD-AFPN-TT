# Automatas-AFD-AFN-AFPD-AFPN-TT
This repository contains the implementation of various types of automata, including AFD (Deterministic Finite Automaton), AFN (Nondeterministic Finite Automaton), AFPD (Pushdown Automaton with Deterministic Control), AFPN (Pushdown Automaton with Nondeterministic Control), and TT (Turing Machine).

Overview
Automata theory is a fundamental concept in computer science and mathematics, studying abstract machines that can perform computations. This repository aims to provide implementations of different types of automata to demonstrate their behavior and functionality.

AFD (Deterministic Finite Automaton)
AFD is a finite state machine where for each state and input symbol, there is exactly one next state. It recognizes regular languages and is commonly used in lexical analysis and pattern matching.

AFN (Nondeterministic Finite Automaton)
AFN is a finite state machine where for each state and input symbol, there can be multiple next states or no next state at all. It recognizes the same set of languages as AFD but allows for greater flexibility in design.

AFPD (Pushdown Automaton with Deterministic Control)
AFPD is an extension of AFD, where the machine has a stack that can be used for additional storage and computation. The control is deterministic, meaning for each state and input symbol, there is exactly one next state. AFPD recognizes context-free languages.

AFPN (Pushdown Automaton with Nondeterministic Control)
AFPN is similar to AFPD, but the control is nondeterministic, allowing for multiple next states or no next state at all for each state and input symbol. AFPN also recognizes context-free languages.

TT (Turing Machine)
TT is a more powerful computational model than the previous automata types. It consists of an infinite tape divided into cells and a read-write head that can move left or right. TT can perform arbitrary computations and recognize recursively enumerable languages.

Team Members
Dylan Rivero Esteves
Miller Estiven Barrera Gonzalez
Cesar Arthuro Lemos Silva
Juan David Tique Triana
Cristian Camilo García Palacios
Installation
To install the necessary packages, run the following command in your terminal:

shell

pip install graphviz

Contributing
[Explain how other developers can contribute to the project, such as guidelines for pull requests and code reviews.]

License
[Specify the license you want to use for your project, for example: MIT License, GNU General Public License, etc.]

Contact
[If you want users to be able to contact you or your team, you can provide contact details here, such as an email address or a link to your GitHub profiles.]
