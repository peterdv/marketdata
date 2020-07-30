.. -*- coding: utf-8; mode: rst; -*-

.. For the Python documentation, 
   this convention is used which you may follow:
    • # with overline, for parts
    • * with overline, for chapters
    • =, for sections
    • -, for subsections
    • ^, for subsubsections
    • ", for paragraphs


.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   Broker
   Brokerages
      A *broker* is an individual or firm that acts
      as an intermediary between an investor and a securities exchange.
      
      Because securities exchanges only accept orders from
      individuals or firms who are members of that exchange,
      individual traders and investors need the services of exchange members.
      Brokers provide that service and are compensated in various ways,
      either through commissions, fees or through being paid
      by the exchange itself.﻿
      
   Broker-Dealer
      A *broker-dealer* is a person or firm in the business of
      buying and selling securities for its own account or
      on behalf of its customers.
      
      The term *broker-dealer* is used in U.S. securities regulation parlance
      to describe stock :term:`Brokerages`
      because most of them act as both agents and principals.

      A brokerage acts as a :term:`Broker` (or agent)
      when it executes orders on behalf of its clients,
      whereas it acts as a dealer, or principal
      when it trades for its own account.

      There are two types of Broker-Dealers:

      1. a *wirehouse*, or a firm that sells its own products to customers; and
      2. an *independent broker-dealer*, or a firm that sells products from outside sources. 
      
   ISIN
   ISIN identifier
   International Securities Identification Number
      The
      `ISO 6166:2013 <https://www.iso.org/standard/44811.html>`_
      *Securities and related financial instruments —
      International securities identification numbering system (ISIN)*      
      defines an international standard
      providing a uniform structure for the identification
      of fungible and non-fungible securities and financial instruments
      using a unique identification number and associated minimum descriptive data.
      
      An *International Securities Identification Number* (ISIN)
      is a code that uniquely identifies a specific securities issue.
      
      The organization that allocates ISINs
      in any particular country
      is the country's respective *National Numbering Agency* (NNA).
      
      The system codes securities that include
      stocks, bonds, options, and futures
      with unique identification numbers.
      
      An ISIN identifier code has 12 alphanumeric characters
      and is structured to include:
      
      1. the country in which the issuing company is headquartered,
      
      2. the specific security identification number,
      
      3. and a final character that acts as a security check to deter fraud or misuse
      
      The first two digits are reserved for
      the security's country of origin or head office of the issuing company.
      The second grouping, which is nine characters long,
      is reserved for the security's unique identifying number.
      The final digit, known as a "check digit," assures the code's authenticity
      and lowers the frequency of errors or misuse.
      
      The middle nine digits of the ISIN system number
      is administered by the local country's *National Numbering Agency*.
      
      An ISIN identifier doesn't include a specific trading venue.
      Another number set, usually,
      a :term:`MIC` (term:`Market Identifier Code`)
      or three-letter exchange code,
      is needed to record location information
      that supplements primary identification codes.
      
   ISO 10383 MIC
   MIC
   Market Identifier Code
      The
      `ISO 10383:2012 <https://www.iso.org/obp/ui/#iso:std:iso:10383:ed-3:v1:en>`_
      *Securities and related financial instruments
      — Codes for exchanges and market identification (MIC)*
      international standard
      specifies a universal method of identifying
      exchanges, trading platforms, regulated or non-regulated markets
      and trade reporting facilities
      as sources of prices and related information in order to facilitate
      automated processing.
      
      It is intended for use in
      any application and communication for identification of places
      
      * where a financial instrument is listed (place of official listing),
      * where a related trade is executed (place of trade), and
      * where trade details are reported (trade reporting facility).
      
      There are different types of MICs.
      
      * A *market segment MIC* identifies a section
	of one of the entities covered by the code
	that specializes in one or more
	specific instruments or is regulated differently.
	Market segment MICs were instituted for more accuracy, according to ISO.
      
      * For each *market segment MIC*, there is a parent MIC,
	also known as an *operating MIC*.
      
      * An *operating MIC*, in turn, identifies the entity that
	operates an exchange, trading platform,
	regulated or non-regulated market,
	or a trade reporting facility in a specific country.
      
      The first letter of any MIC is `X`,
      followed by a three-digit alphanumeric code
      for the market in which a trade takes place. 
      
      Market Identifier Codes (MICs) are to be registered
      at operating/exchange level and at market segment level.
      Market segment MICs and their operating/exchange MIC
      are to be clearly linked in the published lists.
      
      The Registration Authority (RA) for ISO 10383 (MIC) is:
      
      S.W.I.F.T. SC
      Avenue Adèle 1
      1310 La Hulpe
      BELGIUM
      Contact: MIC-ISO10383.Generic@swift.com
      
   Currency Code
   ISO Currency Code
      The
      `ISO 4217:2015 <https://www.iso.org/standard/64758.html>`_
      *Codes for the representation of currencies*
      international standard
      specifies the structure for a three-letter alphabetic code
      and an equivalent three-digit numeric code
      for the representation of currencies.
      For those currencies having minor units,
      it also shows the decimal relationship between such units
      and the currency itself.

      The scope of this International Standard also includes funds and precious metals.

      When ISO currency codes are combined in pairs,
      they make up the symbols and cross rates used in currency trading.

      The first two letters of the code are
      the two letters of the ISO 3166-1 alpha-2 country codes
      and the third is usually the initial of the currency itself.

      Please refer to
      https://www.currency-iso.org/en/home/tables/table-a1.html

   Liquidity Provider
   Market Maker
      A liquidity provider is an individual or institution
      which acts as a market maker in a given asset class.
      This means that the liquidity provider will act as
      both the buyer and seller of a particular asset, thus making a market.
      For instance many stock exchanges have liquidity providers
      who make the commitment to provide liquidity in a given equity.
      These liquidity providers make the commit to providing liquidity
      in the hopes that they will be able to make a profit on the bid-ask spread.

      They quite literally make a market for an asset by
      offering their holdings for sale at any given time
      while simultaneously buying more of them. This pushes the volume of sales higher.
      But it also allows investors to buy shares whenever they want to w
      ithout having to wait for another investor to decide to sell.

      Perhaps the best-known core liquidity providers
      are the institutions that underwrite initial public offerings (IPOs).
      When a company goes public on a stock exchange,
      it selects an underwriter to manage the process.
      The underwriter buys the stock directly from the company
      and then resells it in large batches to large financial institutions,
      which then make the shares available directly to their clients.
   
.. eof
